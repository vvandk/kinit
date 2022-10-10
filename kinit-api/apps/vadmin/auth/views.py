#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/2/24 17:02
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 简要说明

from typing import Optional
from fastapi import APIRouter, Depends, Query
from utils.response import SuccessResponse, ErrorResponse
from . import schemas, crud, models
from core.dependencies import paging, id_list, Params
from apps.vadmin.auth.utils.current import login_auth, Auth

app = APIRouter()


###########################################################
#    用户管理
###########################################################
@app.get("/users/", summary="获取用户列表")
async def get_users(params: Params = Depends(paging), auth: Auth = Depends(login_auth)):
    datas = await crud.UserDal(auth.db).get_datas(params.page, params.limit)
    count = await crud.UserDal(auth.db).get_count()
    return SuccessResponse(datas, count=count)


@app.post("/users/", summary="创建用户")
async def create_user(data: schemas.UserIn, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).create_data(data=data))


@app.delete("/users/", summary="批量删除用户")
async def delete_users(ids: list = Depends(id_list), auth: Auth = Depends(login_auth)):
    await crud.UserDal(auth.db).delete_datas(ids=ids)
    return SuccessResponse("删除成功")


@app.put("/users/{data_id}/", summary="更新用户信息")
async def put_user(data_id: int, data: schemas.User, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).put_data(data_id, data))


@app.get("/users/{data_id}/", summary="获取用户信息")
async def get_user(data_id: int, auth: Auth = Depends(login_auth)):
    model = models.VadminUser
    options = [model.roles]
    schema = schemas.UserOut
    return SuccessResponse(await crud.UserDal(auth.db).get_data(data_id, options, schema))


@app.post("/user/current/reset/password/", summary="重置当前用户密码")
async def user_current_reset_password(data: schemas.ResetPwd, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).reset_current_password(auth.user, data))


@app.post("/user/current/update/info/", summary="更新当前用户基本信息")
async def post_user_current_update_info( data: schemas.UserUpdate, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.UserDal(auth.db).update_current_info(auth.user, data))


@app.get("/user/current/info/", summary="获取当前用户基本信息")
async def get_user_current_info(auth: Auth = Depends(login_auth)):
    return SuccessResponse(schemas.UserSimpleOut.from_orm(auth.user).dict())


###########################################################
#    角色管理
###########################################################
@app.get("/roles/", summary="获取角色列表")
async def get_roles(params: Params = Depends(paging), auth: Auth = Depends(login_auth),
                    name: Optional[str] = Query(None, title="角色名称", description="查询角色名称")):
    datas = await crud.RoleDal(auth.db).get_datas(params.page, params.limit, name=name)
    count = await crud.RoleDal(auth.db).get_count(name=name)
    return SuccessResponse(datas, count=count)


@app.post("/roles/", summary="创建角色信息")
async def create_role(role: schemas.RoleIn, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.RoleDal(auth.db).create_data(data=role))


@app.delete("/roles/", summary="批量删除角色")
async def delete_roles(ids: list = Depends(id_list), auth: Auth = Depends(login_auth)):
    await crud.RoleDal(auth.db).delete_datas(ids)
    return SuccessResponse("删除成功")


@app.put("/roles/{data_id}/", summary="更新角色信息")
async def put_role(data_id: int, data: schemas.RoleIn, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.RoleDal(auth.db).put_data(data_id, data))


@app.get("/roles/options/", summary="获取角色选择项")
async def get_role_options(auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.RoleDal(auth.db).get_select_datas())


@app.get("/roles/{data_id}/", summary="获取角色信息")
async def get_role(data_id: int, auth: Auth = Depends(login_auth)):
    model = models.VadminRole
    options = [model.menus]
    schema = schemas.RoleOut
    return SuccessResponse(await crud.RoleDal(auth.db).get_data(data_id, options, schema))


###########################################################
#    菜单管理
###########################################################
@app.get("/menus/", summary="获取菜单列表")
async def get_menus(auth: Auth = Depends(login_auth)):
    datas = await crud.MenuDal(auth.db).get_tree_list()
    return SuccessResponse(datas)


@app.get("/menus/tree/options/", summary="获取菜单树选择项")
async def get_menus_options(auth: Auth = Depends(login_auth)):
    datas = await crud.MenuDal(auth.db).get_tree_options()
    return SuccessResponse(datas)


@app.get("/menus/role/tree/options/", summary="获取菜单列表树信息，角色权限使用")
async def get_menus_treeselect(auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.MenuDal(auth.db).get_treeselect())


@app.post("/menus/", summary="创建菜单信息")
async def create_menu(menu: schemas.Menu, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.MenuDal(auth.db).create_data(data=menu))


@app.delete("/menus/", summary="批量删除菜单")
async def delete_menus(ids: list = Depends(id_list), auth: Auth = Depends(login_auth)):
    await crud.MenuDal(auth.db).delete_datas(ids)
    return SuccessResponse("删除成功")


@app.delete("/menus/", summary="批量删除菜单")
async def delete_menus(ids: list = Depends(id_list), auth: Auth = Depends(login_auth)):
    await crud.MenuDal(auth.db).delete_datas(ids=ids)
    return SuccessResponse("删除成功")


@app.put("/menus/{data_id}/", summary="更新菜单信息")
async def put_menus(data_id: int, data: schemas.Menu, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.MenuDal(auth.db).put_data(data_id, data))


@app.get("/menus/{data_id}/", summary="获取菜单信息")
async def put_menus(data_id: int, auth: Auth = Depends(login_auth)):
    schema = schemas.MenuSimpleOut
    return SuccessResponse(await crud.MenuDal(auth.db).get_data(data_id, None, schema))


@app.get("/role/menus/tree/{role_id}/", summary="获取菜单列表树信息以及角色菜单权限ID，角色权限使用")
async def get_role_menu_tree(role_id: int, auth: Auth = Depends(login_auth)):
    treeselect = await crud.MenuDal(auth.db).get_treeselect()
    role_menu_tree = await crud.RoleDal(auth.db).get_role_menu_tree(role_id)
    return SuccessResponse({"role_menu_tree": role_menu_tree, "menus": treeselect})
