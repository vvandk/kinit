# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Body
from utils.response import SuccessResponse, ErrorResponse
from . import schemas, crud
from core.dependencies import paging, id_list, Params
from apps.vadmin.auth.utils.current import login_auth, Auth

app = APIRouter()


###########################################################
#    字典类型管理
###########################################################
@app.get("/dict/types/", summary="获取字典类型列表")
async def get_dict_types(params: Params = Depends(paging), auth: Auth = Depends(login_auth),
                         dict_name: Optional[str] = Query(None, title="字典名称", description="查询字典名称")):
    datas = await crud.DictTypeDal(auth.db).get_datas(params.page, params.limit, dict_name=dict_name)
    count = await crud.DictTypeDal(auth.db).get_count(dict_name=dict_name)
    return SuccessResponse(datas, count=count)


@app.post("/dict/types/", summary="创建字典类型")
async def create_dict_types(data: schemas.DictType, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.DictTypeDal(auth.db).create_data(data=data))


@app.delete("/dict/types/", summary="批量删除字典类型")
async def delete_dict_types(ids: list = Depends(id_list), auth: Auth = Depends(login_auth)):
    await crud.DictTypeDal(auth.db).delete_datas(ids=ids)
    return SuccessResponse("删除成功")


@app.post("/dict/types/details/", summary="获取多个字典类型下的字典元素列表")
async def post_dicts_details(auth: Auth = Depends(login_auth),
                             dict_types: List[str] = Body(None, title="字典元素列表", description="查询字典元素列表")):
    datas = await crud.DictTypeDal(auth.db).get_dicts_details(dict_types)
    return SuccessResponse(datas)


@app.get("/dict/types/options/", summary="获取字典类型选择项")
async def get_dicts_options(auth: Auth = Depends(login_auth)):
    datas = await crud.DictTypeDal(auth.db).get_select_datas()
    return SuccessResponse(datas)


@app.put("/dict/types/{data_id}/", summary="更新字典类型")
async def put_dict_types(data_id: int, data: schemas.DictType, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.DictTypeDal(auth.db).put_data(data_id, data))


@app.get("/dict/types/{data_id}/", summary="获取字典类型详细")
async def get_dict_type(data_id: int, auth: Auth = Depends(login_auth)):
    schema = schemas.DictTypeSimpleOut
    return SuccessResponse(await crud.DictTypeDal(auth.db).get_data(data_id, None, schema))


###########################################################
#    字典元素管理
###########################################################
@app.post("/dict/details/", summary="创建字典元素")
async def create_dict_details(data: schemas.DictDetails, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.DictDetailsDal(auth.db).create_data(data=data))


@app.get("/dict/details/", summary="获取单个字典类型下的字典元素列表，分页")
async def get_dict_details(params: Params = Depends(paging), auth: Auth = Depends(login_auth),
                           dict_type_id: Optional[int] = Query(None, title="查询字典类型", description="查询字典类型"),
                           label: Optional[str] = Query(None, title="查询字典标签", description="查询字典标签")):
    if not dict_type_id:
        return ErrorResponse(msg="未获取到字典类型！")
    datas = await crud.DictDetailsDal(auth.db).\
        get_datas(params.page, params.limit, label=label, dict_type_id=dict_type_id)
    count = await crud.DictDetailsDal(auth.db).get_count(label=label, dict_type_id=dict_type_id)
    return SuccessResponse(datas, count=count)


@app.delete("/dict/details/", summary="批量删除字典元素")
async def delete_dict_details(ids: list = Depends(id_list), auth: Auth = Depends(login_auth)):
    await crud.DictDetailsDal(auth.db).delete_datas(ids)
    return SuccessResponse("删除成功")


@app.put("/dict/details/{data_id}/", summary="更新字典元素")
async def put_dict_details(data_id: int, data: schemas.DictDetails, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.DictDetailsDal(auth.db).put_data(data_id, data))


@app.get("/dict/details/{data_id}/", summary="获取字典元素详情")
async def get_dict_detail(data_id: int, auth: Auth = Depends(login_auth)):
    schema = schemas.DictDetailsSimpleOut
    return SuccessResponse(await crud.DictDetailsDal(auth.db).get_data(data_id, None, schema))


###########################################################
#    默认配置
###########################################################
@app.get("/config/default/{key}/", summary="获取系统默认配置")
def system_default_config(key: str):
    data = {
        "sys.user.initPassword": "123456"
    }
    return SuccessResponse(data=data.get(key, None))
