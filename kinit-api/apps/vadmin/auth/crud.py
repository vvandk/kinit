#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/2/24 10:21 
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 增删改查

from typing import Any
from redis.asyncio import Redis
from fastapi import UploadFile
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.exception import CustomException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from core.validator import vali_telephone
from utils.file.aliyun_oss import AliyunOSS, BucketConf
from utils.excel.import_manage import ImportManage, FieldType
from utils.excel.write_xlsx import WriteXlsx
from utils.send_email import EmailSender
from utils.sms.reset_passwd import ResetPasswordSMS
from .params import UserParams
from utils.tools import test_password
from . import models, schemas
from application import settings
from utils.excel.excel_manage import ExcelManage
from apps.vadmin.system import crud as vadmin_system_crud
import copy
from utils import status
from utils.wx.oauth import WXOAuth
from datetime import datetime


class UserDal(DalBase):

    import_headers = [
        {"label": "姓名", "field": "name", "required": True},
        {"label": "昵称", "field": "nickname", "required": False},
        {"label": "手机号", "field": "telephone", "required": True, "rules": [vali_telephone]},
        {"label": "性别", "field": "gender", "required": False},
        {"label": "关联角色", "field": "role_ids", "required": True, "type": FieldType.list},
    ]

    def __init__(self, db: AsyncSession):
        super(UserDal, self).__init__(db, models.VadminUser, schemas.UserSimpleOut)

    async def update_login_info(self, user: models.VadminUser, last_ip: str) -> None:
        """
        更新当前登录信息
        :param user: 用户对象
        :param last_ip: 最近一次登录 IP
        :return:
        """
        user.last_ip = last_ip
        user.last_login = datetime.now()
        await self.db.flush()

    async def create_data(
            self,
            data: schemas.UserIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建用户
        """
        unique = await self.get_data(telephone=data.telephone, v_return_none=True)
        if unique:
            raise CustomException("手机号已存在！", code=status.HTTP_ERROR)
        password = data.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
        data.password = self.model.get_password_hash(password)
        data.avatar = data.avatar if data.avatar else settings.DEFAULT_AVATAR
        obj = self.model(**data.model_dump(exclude={'role_ids'}))
        if data.role_ids:
            roles = await RoleDal(self.db).get_datas(limit=0, id=("in", data.role_ids), v_return_objs=True)
            for role in roles:
                obj.roles.add(role)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.UserUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新用户信息
        """
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.roles)])
        data_dict = jsonable_encoder(data)
        for key, value in data_dict.items():
            if key == "role_ids":
                if value:
                    roles = await RoleDal(self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    if obj.roles:
                        obj.roles.clear()
                    for role in roles:
                        obj.roles.add(role)
                continue
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def reset_current_password(self, user: models.VadminUser, data: schemas.ResetPwd) -> None:
        """
        重置密码
        """
        if data.password != data.password_two:
            raise CustomException(msg="两次密码不一致", code=400)
        result = test_password(data.password)
        if isinstance(result, str):
            raise CustomException(msg=result, code=400)
        user.password = self.model.get_password_hash(data.password)
        user.is_reset_password = True
        await self.flush(user)

    async def update_current_info(self, user: models.VadminUser, data: schemas.UserUpdateBaseInfo) -> Any:
        """
        更新当前用户基本信息
        """
        if data.telephone != user.telephone:
            unique = await self.get_data(telephone=data.telephone, v_return_none=True)
            if unique:
                raise CustomException("手机号已存在！", code=status.HTTP_ERROR)
            else:
                user.telephone = data.telephone
        user.name = data.name
        user.nickname = data.nickname
        user.gender = data.gender
        await self.flush(user)
        return await self.out_dict(user)

    async def export_query_list(self, header: list, params: UserParams) -> dict:
        """
        导出用户查询列表为excel
        """
        datas = await self.get_datas(**params.dict(), v_return_objs=True)
        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []
        options = await vadmin_system_crud.DictTypeDal(self.db).get_dicts_details(["sys_vadmin_gender"])
        for user in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(user, field, "")
                if field == "is_active":
                    value = "可用" if value else "停用"
                elif field == "is_staff":
                    value = "是" if value else "否"
                elif field == "gender":
                    result = list(filter(lambda i: i["value"] == value, options["sys_vadmin_gender"]))
                    value = result[0]["label"] if result else ""
                data.append(value)
            rows.append(data)
        em = ExcelManage()
        em.create_excel("用户列表")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "用户列表.xlsx"}

    async def get_import_headers_options(self) -> None:
        """
        补全表头数据选项
        """
        # 角色选择项
        roles = await RoleDal(self.db).get_datas(limit=0, v_return_objs=True, disabled=False, is_admin=False)
        role_options = self.import_headers[4]
        assert isinstance(role_options, dict)
        role_options["options"] = [{"label": role.name, "value": role.id} for role in roles]

        # 性别选择项
        dict_types = await vadmin_system_crud.DictTypeDal(self.db).get_dicts_details(["sys_vadmin_gender"])
        gender_options = self.import_headers[3]
        assert isinstance(gender_options, dict)
        sys_vadmin_gender = dict_types.get("sys_vadmin_gender")
        gender_options["options"] = [{"label": item["label"], "value": item["value"]} for item in sys_vadmin_gender]

    async def download_import_template(self) -> dict:
        """
        下载用户最新版导入模板
        """
        await self.get_import_headers_options()
        em = WriteXlsx(sheet_name="用户导入模板")
        em.generate_template(copy.deepcopy(self.import_headers))
        em.close()
        return {"url": em.file_url, "filename": "用户导入模板.xlsx"}

    async def import_users(self, file: UploadFile) -> dict:
        """
        批量导入用户数据
        """
        await self.get_import_headers_options()
        im = ImportManage(file, copy.deepcopy(self.import_headers))
        await im.get_table_data()
        im.check_table_data()
        for item in im.success:
            old_data_list = item.pop("old_data_list")
            data = schemas.UserIn(**item)
            try:
                await self.create_data(data)
            except ValueError as e:
                old_data_list.append(e.__str__())
                im.add_error_data(old_data_list)
            except Exception:
                old_data_list.append("创建失败，请联系管理员！")
                im.add_error_data(old_data_list)
        return {
            "success_number": im.success_number,
            "error_number": im.error_number,
            "error_url": im.generate_error_url()
        }

    async def init_password(self, ids: list[int]) -> list:
        """
        初始化所选用户密码
        将用户密码改为系统默认密码，并将初始化密码状态改为false
        """
        users = await self.get_datas(limit=0, id=("in", ids), v_return_objs=True)
        result = []
        for user in users:
            # 重置密码
            data = {"id": user.id, "telephone": user.telephone, "name": user.name, "email": user.email}
            password = user.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
            user.password = self.model.get_password_hash(password)
            user.is_reset_password = False
            self.db.add(user)
            data["reset_password_status"] = True
            data["password"] = password
            result.append(data)
        await self.db.flush()
        return result

    async def init_password_send_sms(self, ids: list[int], rd: Redis) -> list:
        """
        初始化所选用户密码并发送通知短信
        将用户密码改为系统默认密码，并将初始化密码状态改为false
        """
        result = await self.init_password(ids)
        for user in result:
            if not user["reset_password_status"]:
                user["send_sms_status"] = False
                user["send_sms_msg"] = "重置密码失败"
                continue
            password = user.pop("password")
            sms = ResetPasswordSMS([user.get("telephone")], rd)
            try:
                send_result = (await sms.main_async(password=password))[0]
                user["send_sms_status"] = send_result
                user["send_sms_msg"] = "" if send_result else "短信发送失败，请联系管理员"
            except CustomException as e:
                user["send_sms_status"] = False
                user["send_sms_msg"] = e.msg
        return result

    async def init_password_send_email(self, ids: list[int], rd: Redis) -> list:
        """
        初始化所选用户密码并发送通知邮件
        将用户密码改为系统默认密码，并将初始化密码状态改为false
        """
        result = await self.init_password(ids)
        for user in result:
            if not user["reset_password_status"]:
                user["send_sms_status"] = False
                user["send_sms_msg"] = "重置密码失败"
                continue
            password: str = user.pop("password")
            email: str = user.get("email", None)
            if email:
                subject = "密码已重置"
                body = f"您好，您的密码已经重置为{password}，请及时登录并修改密码。"
                es = EmailSender(rd)
                try:
                    send_result = await es.send_email([email], subject, body)
                    user["send_sms_status"] = send_result
                    user["send_sms_msg"] = "" if send_result else "短信发送失败，请联系管理员"
                except CustomException as e:
                    user["send_sms_status"] = False
                    user["send_sms_msg"] = e.msg
            else:
                user["send_sms_status"] = False
                user["send_sms_msg"] = "未获取到邮箱地址"
        return result

    async def update_current_avatar(self, user: models.VadminUser, file: UploadFile) -> str:
        """
        更新当前用户头像
        """
        result = await AliyunOSS(BucketConf(**settings.ALIYUN_OSS)).upload_image("avatar", file)
        user.avatar = result
        await self.flush(user)
        return result

    async def update_wx_server_openid(self, code: str, user: models.VadminUser, redis: Redis) -> bool:
        """
        更新用户服务端微信平台openid
        """
        wx = WXOAuth(redis, 0)
        openid = await wx.parsing_openid(code)
        if not openid:
            return False
        user.is_wx_server_openid = True
        user.wx_server_openid = openid
        await self.flush(user)
        return True

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多个用户，软删除
        删除后清空所关联的角色
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        options = [joinedload(self.model.roles)]
        objs = await self.get_datas(limit=0, id=("in", ids), v_options=options, v_return_objs=True)
        for obj in objs:
            if obj.roles:
                obj.roles.clear()
        return await super(UserDal, self).delete_datas(ids, v_soft, **kwargs)


class RoleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RoleDal, self).__init__(db, models.VadminRole, schemas.RoleSimpleOut)

    async def create_data(
            self,
            data: schemas.RoleIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """创建数据"""
        obj = self.model(**data.model_dump(exclude={'menu_ids'}))
        if data.menu_ids:
            menus = await MenuDal(db=self.db).get_datas(limit=0, id=("in", data.menu_ids), v_return_objs=True)
            for menu in menus:
                obj.menus.add(menu)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.RoleIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """更新单个数据"""
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.menus)])
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            if key == "menu_ids":
                if value:
                    menus = await MenuDal(db=self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    if obj.menus:
                        obj.menus.clear()
                    for menu in menus:
                        obj.menus.add(menu)
                continue
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def get_role_menu_tree(self, role_id: int) -> list:
        role = await self.get_data(role_id, v_options=[joinedload(self.model.menus)])
        return [i.id for i in role.menus]

    async def get_select_datas(self) -> list:
        """获取选择数据，全部数据"""
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.RoleOptionsOut.model_validate(i).model_dump() for i in queryset.all()]

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多个角色，硬删除
        如果存在用户关联则无法删除
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        user_count = await UserDal(self.db).get_count(v_join=[["roles"]], v_where=[models.VadminRole.id.in_(ids)])
        if user_count > 0:
            raise CustomException("无法删除存在用户关联的角色", code=400)
        return await super(RoleDal, self).delete_datas(ids, v_soft, **kwargs)


class MenuDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(MenuDal, self).__init__(db, models.VadminMenu, schemas.MenuSimpleOut)

    async def get_tree_list(self, mode: int) -> list:
        """
        1：获取菜单树列表
        2：获取菜单树选择项，添加/修改菜单时使用
        3：获取菜单树列表，角色添加菜单权限时使用
        """
        if mode == 3:
            sql = select(self.model).where(self.model.disabled == 0, self.model.is_delete == False)
        else:
            sql = select(self.model).where(self.model.is_delete == False)
        queryset = await self.db.scalars(sql)
        datas = list(queryset.all())
        roots = filter(lambda i: not i.parent_id, datas)
        if mode == 1:
            menus = self.generate_tree_list(datas, roots)
        elif mode == 2 or mode == 3:
            menus = self.generate_tree_options(datas, roots)
        else:
            raise CustomException("获取菜单失败，无可用选项", code=400)
        return self.menus_order(menus)

    async def get_routers(self, user: models.VadminUser) -> list:
        """
        获取路由表
        declare interface AppCustomRouteRecordRaw extends Omit<RouteRecordRaw, 'meta'> {
            name: string
            meta: RouteMeta
            component: string
            path: string
            redirect: string
            children?: AppCustomRouteRecordRaw[]
        }
        """
        if any([i.is_admin for i in user.roles]):
            sql = select(self.model) \
                .where(self.model.disabled == 0, self.model.menu_type != "2", self.model.is_delete == False)
            queryset = await self.db.scalars(sql)
            datas = list(queryset.all())
        else:
            options = [joinedload(models.VadminUser.roles).subqueryload(models.VadminRole.menus)]
            user = await UserDal(self.db).get_data(user.id, v_options=options)
            datas = set()
            for role in user.roles:
                for menu in role.menus:
                    # 该路由没有被禁用，并且菜单不是按钮
                    if not menu.disabled and menu.menu_type != "2":
                        datas.add(menu)
        roots = filter(lambda i: not i.parent_id, datas)
        menus = self.generate_router_tree(datas, roots)
        return self.menus_order(menus)

    def generate_router_tree(self, menus: list[models.VadminMenu], nodes: filter, name: str = "") -> list:
        """
        生成路由树

        menus: 总菜单列表
        nodes：节点菜单列表
        name：name拼接，切记Name不能重复
        """
        data = []
        for root in nodes:
            router = schemas.RouterOut.model_validate(root)
            router.name = name + "".join(name.capitalize() for name in router.path.split("/"))
            router.meta = schemas.Meta(
                title=root.title,
                icon=root.icon,
                hidden=root.hidden,
                alwaysShow=root.alwaysShow,
                noCache=root.noCache
            )
            if root.menu_type == "0":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_router_tree(menus, sons, router.name)
            data.append(router.model_dump())
        return data

    def generate_tree_list(self, menus: list[models.VadminMenu], nodes: filter) -> list:
        """
        生成菜单树列表

        menus: 总菜单列表
        nodes：每层节点菜单列表
        """
        data = []
        for root in nodes:
            router = schemas.TreeListOut.model_validate(root)
            if root.menu_type == "0" or root.menu_type == "1":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_tree_list(menus, sons)
            data.append(router.model_dump())
        return data

    def generate_tree_options(self, menus: list[models.VadminMenu], nodes: filter) -> list:
        """
        生成菜单树选择项

        menus: 总菜单列表
        nodes：每层节点菜单列表
        """
        data = []
        for root in nodes:
            router = {"value": root.id, "label": root.title, "order": root.order}
            if root.menu_type == "0" or root.menu_type == "1":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router["children"] = self.generate_tree_options(menus, sons)
            data.append(router)
        return data

    @classmethod
    def menus_order(cls, datas: list, order: str = "order", children: str = "children") -> list:
        """
        菜单排序
        """
        result = sorted(datas, key=lambda menu: menu[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda menu: menu[order])
        return result

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多个菜单
        如果存在角色关联则无法删除
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        count = await RoleDal(self.db).get_count(v_join=[["menus"]], v_where=[self.model.id.in_(ids)])
        if count > 0:
            raise CustomException("无法删除存在角色关联的菜单", code=400)
        await super(MenuDal, self).delete_datas(ids, v_soft, **kwargs)


class TestDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(TestDal, self).__init__(db, models.VadminUser, schemas.UserSimpleOut)

    async def test(self):
        # print("-----------------------开始------------------------")
        options = [joinedload(self.model.roles)]
        v_join = [[self.model.roles]]
        v_where = [self.model.id == 1, models.VadminRole.id == 1]
        v_start_sql = select(self.model)
        result, count = await self.get_datas(
            v_start_sql=v_start_sql,
            v_join=v_join,
            v_options=options,
            v_where=v_where,
            v_return_count=True
        )
        if result:
            print(result)
            print(count)
        # print("-----------------------结束------------------------")
