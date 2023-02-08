#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/2/24 17:02
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 简要说明

from fastapi import APIRouter, Depends, Body, UploadFile, Request
from utils.response import SuccessResponse, ErrorResponse
from . import schemas, crud, models
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import login_auth, Auth, get_user_permissions, full_admin
from .params import UserParams, RoleParams

app = APIRouter()


###########################################################
#    用户管理
###########################################################
@app.get("/users/", summary="获取用户列表")
async def get_users(params: UserParams = Depends(), auth: Auth = Depends(login_auth)):
    datas = await crud.UserDal(auth.db).get_datas(**params.dict())
    count = await crud.UserDal(auth.db).get_count(**params.to_count())
    return SuccessResponse(datas, count=count)


@app.post("/users/", summary="创建用户")
async def create_user(data: schemas.UserIn, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).create_data(data=data))


@app.delete("/users/", summary="批量删除用户")
async def delete_users(ids: IdList = Depends(), auth: Auth = Depends(login_auth)):
    if auth.user.id in ids.ids:
        return ErrorResponse("不能删除当前登录用户")
    elif 1 in ids.ids:
        return ErrorResponse("不能删除超级管理员用户")
    await crud.UserDal(auth.db).delete_datas(ids=ids.ids, soft=True)
    return SuccessResponse("删除成功")


@app.put("/users/{data_id}/", summary="更新用户信息")
async def put_user(data_id: int, data: schemas.User, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).put_data(data_id, data))


@app.get("/users/{data_id}/", summary="获取用户信息")
async def get_user(data_id: int, auth: Auth = Depends(login_auth)):
    model = models.VadminUser
    options = [model.roles]
    schema = schemas.UserOut
    return SuccessResponse(await crud.UserDal(auth.db).get_data(data_id, options, v_schema=schema))


@app.post("/user/current/reset/password/", summary="重置当前用户密码")
async def user_current_reset_password(data: schemas.ResetPwd, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).reset_current_password(auth.user, data))


@app.post("/user/current/update/info/", summary="更新当前用户基本信息")
async def post_user_current_update_info(data: schemas.UserUpdate, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).update_current_info(auth.user, data))


@app.post("/user/current/update/avatar/", summary="更新当前用户头像")
async def post_user_current_update_avatar(file: UploadFile, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).update_current_avatar(auth.user, file))


@app.get("/user/current/info/", summary="获取当前用户基本信息")
async def get_user_current_info(auth: Auth = Depends(full_admin)):
    result = schemas.UserOut.from_orm(auth.user).dict()
    result["permissions"] = await get_user_permissions(auth.user)
    return SuccessResponse(result)


@app.post("/user/export/query/list/to/excel/", summary="导出用户查询列表为excel")
async def post_user_export_query_list(
        header: list = Body(..., title="表头与对应字段"),
        params: UserParams = Depends(),
        auth: Auth = Depends(login_auth)
):
    return SuccessResponse(await crud.UserDal(auth.db).export_query_list(header, params))


@app.get("/user/download/import/template/", summary="下载最新批量导入用户模板")
async def get_user_download_new_import_template(auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).download_import_template())


@app.post("/import/users/", summary="批量导入用户")
async def post_import_users(file: UploadFile, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).import_users(file))


@app.post("/users/init/password/send/sms/", summary="初始化所选用户密码并发送通知短信")
async def post_users_init_password(request: Request, ids: IdList = Depends(), auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).init_password_send_sms(ids.ids, request.app.state.redis))


###########################################################
#    角色管理
###########################################################
@app.get("/roles/", summary="获取角色列表")
async def get_roles(params: RoleParams = Depends(), auth: Auth = Depends(login_auth)):
    datas = await crud.RoleDal(auth.db).get_datas(**params.dict())
    count = await crud.RoleDal(auth.db).get_count(**params.to_count())
    return SuccessResponse(datas, count=count)


@app.post("/roles/", summary="创建角色信息")
async def create_role(role: schemas.RoleIn, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.RoleDal(auth.db).create_data(data=role))


@app.delete("/roles/", summary="批量删除角色")
async def delete_roles(ids: IdList = Depends(), auth: Auth = Depends(login_auth)):
    if 1 in ids.ids:
        return ErrorResponse("不能删除管理员角色")
    await crud.RoleDal(auth.db).delete_datas(ids.ids, soft=True)
    return SuccessResponse("删除成功")


@app.put("/roles/{data_id}/", summary="更新角色信息")
async def put_role(data_id: int, data: schemas.RoleIn, auth: Auth = Depends(login_auth)):
    if 1 == data_id:
        return ErrorResponse("不能修改管理员角色")
    return SuccessResponse(await crud.RoleDal(auth.db).put_data(data_id, data))


@app.get("/roles/options/", summary="获取角色选择项")
async def get_role_options(auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.RoleDal(auth.db).get_select_datas())


@app.get("/roles/{data_id}/", summary="获取角色信息")
async def get_role(data_id: int, auth: Auth = Depends(login_auth)):
    model = models.VadminRole
    options = [model.menus]
    schema = schemas.RoleOut
    return SuccessResponse(await crud.RoleDal(auth.db).get_data(data_id, options, v_schema=schema))


###########################################################
#    菜单管理
###########################################################
@app.get("/menus/", summary="获取菜单列表")
async def get_menus(auth: Auth = Depends(login_auth)):
    datas = await crud.MenuDal(auth.db).get_tree_list(mode=1)
    return SuccessResponse(datas)


@app.get("/menus/tree/options/", summary="获取菜单树选择项，添加/修改菜单时使用")
async def get_menus_options(auth: Auth = Depends(login_auth)):
    datas = await crud.MenuDal(auth.db).get_tree_list(mode=2)
    return SuccessResponse(datas)


@app.get("/menus/role/tree/options/", summary="获取菜单列表树信息，角色权限使用")
async def get_menus_treeselect(auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.MenuDal(auth.db).get_tree_list(mode=3))


@app.post("/menus/", summary="创建菜单信息")
async def create_menu(menu: schemas.Menu, auth: Auth = Depends(login_auth)):
    if menu.parent_id:
        menu.alwaysShow = False
    return SuccessResponse(await crud.MenuDal(auth.db).create_data(data=menu))


@app.delete("/menus/", summary="批量删除菜单")
async def delete_menus(ids: IdList = Depends(), auth: Auth = Depends(login_auth)):
    await crud.MenuDal(auth.db).delete_datas(ids.ids, soft=True)
    return SuccessResponse("删除成功")


@app.put("/menus/{data_id}/", summary="更新菜单信息")
async def put_menus(data_id: int, data: schemas.Menu, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.MenuDal(auth.db).put_data(data_id, data))


@app.get("/menus/{data_id}/", summary="获取菜单信息")
async def put_menus(data_id: int, auth: Auth = Depends(login_auth)):
    schema = schemas.MenuSimpleOut
    return SuccessResponse(await crud.MenuDal(auth.db).get_data(data_id, None, v_schema=schema))


@app.get("/role/menus/tree/{role_id}/", summary="获取菜单列表树信息以及角色菜单权限ID，角色权限使用")
async def get_role_menu_tree(role_id: int, auth: Auth = Depends(login_auth)):
    treeselect = await crud.MenuDal(auth.db).get_tree_list(mode=3)
    role_menu_tree = await crud.RoleDal(auth.db).get_role_menu_tree(role_id)
    return SuccessResponse({"role_menu_tree": role_menu_tree, "menus": treeselect})
