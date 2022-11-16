# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

# UploadFile 库依赖：pip install python-multipart
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Body, UploadFile, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from application.settings import ALIYUN_OSS
from core.database import db_getter
from utils.aliyun_oss import AliyunOSS, BucketConf
from utils.aliyun_sms import AliyunSMS
from utils.file_manage import FileManage
from utils.response import SuccessResponse, ErrorResponse
from . import schemas, crud, models
from core.dependencies import Paging, IdList
from apps.vadmin.auth.utils.current import login_auth, Auth
from .params import DictTypeParams, DictDetailParams

app = APIRouter()


###########################################################
#    字典类型管理
###########################################################
@app.get("/dict/types/", summary="获取字典类型列表")
async def get_dict_types(params: DictTypeParams = Depends(), auth: Auth = Depends(login_auth)):
    datas = await crud.DictTypeDal(auth.db).get_datas(**params.dict())
    count = await crud.DictTypeDal(auth.db).get_count(**params.to_count())
    return SuccessResponse(datas, count=count)


@app.post("/dict/types/", summary="创建字典类型")
async def create_dict_types(data: schemas.DictType, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.DictTypeDal(auth.db).create_data(data=data))


@app.delete("/dict/types/", summary="批量删除字典类型")
async def delete_dict_types(ids: IdList = Depends(), auth: Auth = Depends(login_auth)):
    await crud.DictTypeDal(auth.db).delete_datas(ids=ids.ids)
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
async def get_dict_details(params: DictDetailParams = Depends(), auth: Auth = Depends(login_auth)):
    if not params.dict_type_id:
        return ErrorResponse(msg="未获取到字典类型！")
    datas = await crud.DictDetailsDal(auth.db).get_datas(**params.dict())
    count = await crud.DictDetailsDal(auth.db).get_count(**params.to_count())
    return SuccessResponse(datas, count=count)


@app.delete("/dict/details/", summary="批量删除字典元素")
async def delete_dict_details(ids: IdList = Depends(), auth: Auth = Depends(login_auth)):
    await crud.DictDetailsDal(auth.db).delete_datas(ids.ids)
    return SuccessResponse("删除成功")


@app.put("/dict/details/{data_id}/", summary="更新字典元素")
async def put_dict_details(data_id: int, data: schemas.DictDetails, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.DictDetailsDal(auth.db).put_data(data_id, data))


@app.get("/dict/details/{data_id}/", summary="获取字典元素详情")
async def get_dict_detail(data_id: int, auth: Auth = Depends(login_auth)):
    schema = schemas.DictDetailsSimpleOut
    return SuccessResponse(await crud.DictDetailsDal(auth.db).get_data(data_id, None, schema))


###########################################################
#    文件上传管理
###########################################################
@app.post("/upload/image/to/oss/", summary="上传图片到阿里云OSS")
async def upload_image_to_oss(file: UploadFile, path: str = Form(...)):
    manage = FileManage(file, path)
    result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_image(manage.path, file)
    if not result:
        return ErrorResponse(msg="上传失败")
    return SuccessResponse(result)


@app.post("/upload/image/to/local/", summary="上传图片到本地")
async def upload_image_to_local(file: UploadFile, path: str = Form(...)):
    manage = FileManage(file, path)
    path = await manage.save_image_local()
    return SuccessResponse(path)


###########################################################
#    短信服务管理
###########################################################
@app.post("/sms/send/", summary="发送短信验证码（阿里云服务）")
async def sms_send(request: Request, telephone: str):
    sms = AliyunSMS(request.app.state.redis, telephone)
    return SuccessResponse(await sms.main_async(AliyunSMS.Scene.login))


###########################################################
#    系统配置管理
###########################################################
@app.get("/settings/tabs/", summary="获取系统配置标签列表")
async def get_settings_tabs(classify: str, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.SettingsTabDal(auth.db).get_datas(limit=0, classify=classify))


@app.get("/settings/tabs/values/", summary="获取系统配置标签下的信息")
async def get_settings_tabs_values(tab_id: int, auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.SettingsDal(auth.db).get_tab_values(tab_id=tab_id))


@app.put("/settings/tabs/values/", summary="更新系统配置信息")
async def put_settings_tabs_values(datas: dict = Body(...), auth: Auth = Depends(login_auth)):
    return SuccessResponse(await crud.SettingsDal(auth.db).update_datas(datas))


@app.get("/settings/classifys/", summary="获取系统配置分类下的所有显示标签信息")
async def get_settings_classifys(classify: str, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.SettingsTabDal(db).get_classify_tab_values([classify]))
