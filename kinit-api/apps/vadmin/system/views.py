# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from redis.asyncio import Redis
from fastapi import APIRouter, Depends, Body, UploadFile, Form, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from application.settings import ALIYUN_OSS
from core.database import db_getter, redis_getter, mongo_getter
from utils.file.aliyun_oss import AliyunOSS, BucketConf
from utils.file.file_manage import FileManage
from utils.response import SuccessResponse, ErrorResponse
from utils.sms.code import CodeSMS
from . import schemas, crud
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth, OpenAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from .params import DictTypeParams, DictDetailParams, TaskParams
from apps.vadmin.auth import crud as vadmin_auth_crud
from .params.task import TaskRecordParams

app = APIRouter()


###########################################################
#    字典类型管理
###########################################################
@app.get("/dict/types", summary="获取字典类型列表")
async def get_dict_types(p: DictTypeParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.DictTypeDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/dict/types", summary="创建字典类型")
async def create_dict_types(data: schemas.DictType, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictTypeDal(auth.db).create_data(data=data))


@app.delete("/dict/types", summary="批量删除字典类型")
async def delete_dict_types(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DictTypeDal(auth.db).delete_datas(ids=ids.ids)
    return SuccessResponse("删除成功")


@app.post("/dict/types/details", summary="获取多个字典类型下的字典元素列表")
async def post_dicts_details(
        auth: Auth = Depends(AllUserAuth()),
        dict_types: list[str] = Body(None, title="字典元素列表", description="查询字典元素列表")
):
    datas = await crud.DictTypeDal(auth.db).get_dicts_details(dict_types)
    return SuccessResponse(datas)


@app.get("/dict/types/options", summary="获取字典类型选择项")
async def get_dicts_options(auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictTypeDal(auth.db).get_select_datas())


@app.put("/dict/types/{data_id}", summary="更新字典类型")
async def put_dict_types(data_id: int, data: schemas.DictType, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictTypeDal(auth.db).put_data(data_id, data))


@app.get("/dict/types/{data_id}", summary="获取字典类型详细")
async def get_dict_type(data_id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.DictTypeSimpleOut
    return SuccessResponse(await crud.DictTypeDal(auth.db).get_data(data_id, v_schema=schema))


###########################################################
#    字典元素管理
###########################################################
@app.post("/dict/details", summary="创建字典元素")
async def create_dict_details(data: schemas.DictDetails, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictDetailsDal(auth.db).create_data(data=data))


@app.get("/dict/details", summary="获取单个字典类型下的字典元素列表，分页")
async def get_dict_details(params: DictDetailParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.DictDetailsDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.delete("/dict/details", summary="批量删除字典元素", description="硬删除")
async def delete_dict_details(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DictDetailsDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/dict/details/{data_id}", summary="更新字典元素")
async def put_dict_details(data_id: int, data: schemas.DictDetails, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.DictDetailsDal(auth.db).put_data(data_id, data))


@app.get("/dict/details/{data_id}", summary="获取字典元素详情")
async def get_dict_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.DictDetailsSimpleOut
    return SuccessResponse(await crud.DictDetailsDal(auth.db).get_data(data_id, v_schema=schema))


###########################################################
#    文件上传管理
###########################################################
@app.post("/upload/image/to/oss", summary="上传图片到阿里云OSS")
async def upload_image_to_oss(file: UploadFile, path: str = Form(...)):
    result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_image(path, file)
    return SuccessResponse(result)


@app.post("/upload/video/to/oss", summary="上传视频到阿里云OSS")
async def upload_video_to_oss(file: UploadFile, path: str = Form(...)):
    result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_video(path, file)
    return SuccessResponse(result)


@app.post("/upload/file/to/oss", summary="上传文件到阿里云OSS")
async def upload_file_to_oss(file: UploadFile, path: str = Form(...)):
    result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_file(path, file)
    return SuccessResponse(result)


@app.post("/upload/image/to/local", summary="上传图片到本地")
async def upload_image_to_local(file: UploadFile, path: str = Form(...)):
    manage = FileManage(file, path)
    path = await manage.save_image_local()
    return SuccessResponse(path)


###########################################################
#    短信服务管理
###########################################################
@app.post("/sms/send", summary="发送短信验证码（阿里云服务）")
async def sms_send(telephone: str, rd: Redis = Depends(redis_getter), auth: Auth = Depends(OpenAuth())):
    user = await vadmin_auth_crud.UserDal(auth.db).get_data(telephone=telephone, v_return_none=True)
    if not user:
        return ErrorResponse("手机号不存在！")
    sms = CodeSMS(telephone, rd)
    return SuccessResponse(await sms.main_async())


###########################################################
#    系统配置管理
###########################################################
@app.post("/settings/tabs", summary="获取系统配置标签列表")
async def get_settings_tabs(classifys: list[str] = Body(...), auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.SettingsTabDal(auth.db).get_datas(limit=0, classify=("in", classifys)))


@app.get("/settings/tabs/values", summary="获取系统配置标签下的信息")
async def get_settings_tabs_values(tab_id: int, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.SettingsDal(auth.db).get_tab_values(tab_id=tab_id))


@app.put("/settings/tabs/values", summary="更新系统配置信息")
async def put_settings_tabs_values(
        request: Request,
        datas: dict = Body(...),
        auth: Auth = Depends(FullAdminAuth())
):
    return SuccessResponse(await crud.SettingsDal(auth.db).update_datas(datas, request))


@app.get("/settings/base/config", summary="获取系统基础配置", description="每次进入系统中时使用")
async def get_setting_base_config(db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.SettingsDal(db).get_base_config())


@app.get("/settings/privacy", summary="获取隐私协议")
async def get_settings_privacy(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse((await crud.SettingsDal(auth.db).get_data(config_key="web_privacy")).config_value)


@app.get("/settings/agreement", summary="获取用户协议")
async def get_settings_agreement(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse((await crud.SettingsDal(auth.db).get_data(config_key="web_agreement")).config_value)


###########################################################
#    定时任务管理
###########################################################
@app.get("/tasks", summary="获取定时任务列表")
async def get_tasks(
        p: TaskParams = Depends(),
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        auth: Auth = Depends(AllUserAuth())
):
    datas, count = await crud.TaskDal(db).get_tasks(**p.dict())
    return SuccessResponse(datas, count=count)


@app.post("/tasks", summary="添加定时任务")
async def post_tasks(
        data: schemas.Task,
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        rd: Redis = Depends(redis_getter),
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(db).create_task(rd, data))


@app.put("/tasks", summary="更新定时任务")
async def put_tasks(
        _id: str,
        data: schemas.Task,
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        rd: Redis = Depends(redis_getter),
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(db).put_task(rd, _id, data))


@app.delete("/tasks", summary="删除单个定时任务")
async def delete_task(
        _id: str,
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(db).delete_task(_id))


@app.get("/task", summary="获取定时任务详情")
async def get_task(
        _id: str,
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(db).get_task(_id, v_schema=schemas.TaskSimpleOut))


@app.post("/task", summary="执行一次定时任务")
async def run_once_task(
        _id: str,
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        rd: Redis = Depends(redis_getter),
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TaskDal(db).run_once_task(rd, _id))


###########################################################
#    定时任务分组管理
###########################################################
@app.get("/task/group/options", summary="获取定时任务分组选择项列表")
async def get_task_group_options(db: AsyncIOMotorDatabase = Depends(mongo_getter), auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.TaskGroupDal(db).get_datas(limit=0))


###########################################################
#    定时任务调度日志
###########################################################
@app.get("/task/records", summary="获取定时任务调度日志列表")
async def get_task_records(
        p: TaskRecordParams = Depends(),
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        auth: Auth = Depends(AllUserAuth())
):
    count = await crud.TaskRecordDal(db).get_count(**p.to_count())
    datas = await crud.TaskRecordDal(db).get_datas(**p.dict())
    return SuccessResponse(datas, count=count)
