#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/2/24 10:21 
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 增删改查

from typing import List

from aioredis import Redis
from fastapi import UploadFile
from core.exception import CustomException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from core.validator import vali_telephone
from utils.aliyun_oss import AliyunOSS, BucketConf
from utils.aliyun_sms import AliyunSMS
from utils.excel.import_manage import ImportManage, FieldType
from utils.excel.write_xlsx import WriteXlsx
from utils.file_manage import FileManage
from .params import UserParams
from utils.tools import test_password
from . import models, schemas
from application import settings
from utils.excel.excel_manage import ExcelManage
from apps.vadmin.system import crud as vadminSystemCRUD
import copy
from utils import status


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

    async def create_data(self, data: schemas.UserIn, return_obj: bool = False, options: list = None, schema=None):
        """
        创建用户
        """
        unique = await self.get_data(telephone=data.telephone, v_return_none=True)
        if unique:
            raise CustomException("手机号已存在！", code=status.HTTP_ERROR)
        password = data.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
        data.password = self.model.get_password_hash(password)
        obj = self.model(**data.dict(exclude={'role_ids'}))
        for data_id in data.role_ids:
            obj.roles.append(await RoleDal(db=self.db).get_data(data_id=data_id))
        await self.flush(obj)
        if options:
            obj = await self.get_data(obj.id, options=options)
        if return_obj:
            return obj
        if schema:
            return schema.from_orm(obj).dict()
        return self.out_dict(obj)

    async def reset_current_password(self, user: models.VadminUser, data: schemas.ResetPwd):
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
        return True

    async def update_current_info(self, user: models.VadminUser, data: schemas.UserUpdate):
        """
        更新当前用户信息
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
        return self.out_dict(user)

    async def export_query_list(self, header: list, params: UserParams):
        """
        导出用户查询列表为excel
        """
        datas = await self.get_datas(**params.dict(), v_return_objs=True)
        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []
        options = await vadminSystemCRUD.DictTypeDal(self.db).get_dicts_details(["sys_vadmin_gender"])
        for user in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(user, field, "")
                if field == "is_active":
                    value = "可用" if value else "停用"
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

    async def get_import_headers_options(self):
        """
        补全表头数据选项
        """
        # 角色选择项
        roles = await RoleDal(self.db).get_datas(limit=0, v_return_objs=True, disabled=False, is_admin=False)
        role_options = self.import_headers[4]
        assert isinstance(role_options, dict)
        role_options["options"] = [{"label": role.name, "value": role.id} for role in roles]

        # 性别选择项
        dict_types = await vadminSystemCRUD.DictTypeDal(self.db).get_dicts_details(["sys_vadmin_gender"])
        gender_options = self.import_headers[3]
        assert isinstance(gender_options, dict)
        sys_vadmin_gender = dict_types.get("sys_vadmin_gender")
        gender_options["options"] = [{"label": item["label"], "value": item["value"]} for item in sys_vadmin_gender]

    async def download_import_template(self):
        """
        下载用户最新版导入模板
        """
        await self.get_import_headers_options()
        em = WriteXlsx(sheet_name="用户导入模板")
        em.generate_template(copy.deepcopy(self.import_headers))
        em.close()
        return {"url": em.file_url, "filename": "用户导入模板.xlsx"}

    async def import_users(self, file: UploadFile):
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

    async def init_password_send_sms(self, ids: List[int], rd: Redis):
        """
        初始化所选用户密码并发送通知短信
        将用户密码改为系统默认密码，并将初始化密码状态改为false
        """
        users = await self.get_datas(limit=0, id=("in", ids), v_return_objs=True)
        result = []
        for user in users:
            # 重置密码
            data = {"id": user.id, "telephone": user.telephone, "name": user.name}
            password = user.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
            user.password = self.model.get_password_hash(password)
            user.is_reset_password = False
            self.db.add(user)
            data["reset_password_status"] = True
            data["password"] = password
            result.append(data)
        await self.db.flush()
        for user in result:
            if not user["reset_password_status"]:
                user["send_sms_status"] = False
                user["send_sms_msg"] = "重置密码失败"
                continue
            password = user.pop("password")
            sms = AliyunSMS(rd, user.get("telephone"))
            try:
                send_result = await sms.main_async(AliyunSMS.Scene.reset_password, password=password)
                user["send_sms_status"] = send_result
                user["send_sms_msg"] = "" if send_result else "发送失败，请联系管理员"
            except CustomException as e:
                user["send_sms_status"] = False
                user["send_sms_msg"] = e.msg
        return result

    async def update_current_avatar(self, user: models.VadminUser, file: UploadFile):
        """
        更新当前用户头像
        """
        manage = FileManage(file, "avatar")
        result = await AliyunOSS(BucketConf(**settings.ALIYUN_OSS)).upload_image(manage.path, file)
        if not result:
            raise CustomException(msg="上传失败", code=status.HTTP_ERROR)
        user.avatar = result
        await self.flush(user)
        return result


class RoleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RoleDal, self).__init__(db, models.VadminRole, schemas.RoleSimpleOut)

    async def create_data(self, data: schemas.RoleIn, return_obj: bool = False, options: list = None, schema=None):
        """创建数据"""
        obj = self.model(**data.dict(exclude={'menu_ids'}))
        for data_id in data.menu_ids:
            obj.menus.append(await MenuDal(db=self.db).get_data(data_id=data_id))
        await self.flush(obj)
        if options:
            obj = await self.get_data(obj.id, options=options)
        if return_obj:
            return obj
        if schema:
            return schema.from_orm(obj).dict()
        return self.out_dict(await self.get_data(obj.id))

    async def put_data(self, data_id: int, data: schemas.RoleIn, return_obj: bool = False, options: list = None,
                       schema=None):
        """更新单个数据"""
        obj = await self.get_data(data_id, options=[self.model.menus])
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            if key == "menu_ids":
                if obj.menus:
                    obj.menus.clear()
                for data_id in value:
                    obj.menus.append(await MenuDal(db=self.db).get_data(data_id=data_id))
                continue
            setattr(obj, key, value)
        await self.db.flush()
        await self.db.refresh(obj)
        if return_obj:
            return obj
        if schema:
            return schema.from_orm(obj).dict()
        return self.out_dict(obj)

    async def get_role_menu_tree(self, role_id: int):
        role = await self.get_data(role_id, options=[self.model.menus])
        return [i.id for i in role.menus]

    async def get_select_datas(self):
        """获取选择数据，全部数据"""
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.RoleSelectOut.from_orm(i).dict() for i in queryset.scalars().all()]


class MenuDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(MenuDal, self).__init__(db, models.VadminMenu, schemas.MenuSimpleOut)

    async def get_tree_list(self, mode: int):
        """
        1：获取菜单树列表
        2：获取菜单树选择项，添加/修改菜单时使用
        3：获取菜单树列表，角色添加菜单权限时使用
        """
        if mode == 3:
            sql = select(self.model).where(self.model.disabled == 0)
        else:
            sql = select(self.model)
        queryset = await self.db.execute(sql)
        datas = queryset.scalars().all()
        roots = filter(lambda i: not i.parent_id, datas)
        if mode == 1:
            menus = self.generate_tree_list(datas, roots)
        elif mode == 2 or mode == 3:
            menus = self.generate_tree_options(datas, roots)
        else:
            raise CustomException("获取菜单失败，无可用选项", code=400)
        return self.menus_order(menus)

    async def get_routers(self, user: models.VadminUser):
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
            sql = select(self.model).where(self.model.disabled == 0, self.model.menu_type != "2")
            queryset = await self.db.execute(sql)
            datas = queryset.scalars().all()
        else:
            datas = set()
            for role in user.roles:
                role_obj = await RoleDal(self.db).get_data(role.id, options=[models.VadminRole.menus])
                for menu in role_obj.menus:
                    # 该路由没有被禁用，并且菜单不是按钮
                    if not menu.disabled and menu.menu_type != "2":
                        datas.add(menu)
        roots = filter(lambda i: not i.parent_id, datas)
        menus = self.generate_router_tree(datas, roots)
        return self.menus_order(menus)

    def generate_router_tree(self, menus: List[models.VadminMenu], nodes: filter, name: str = "") -> list:
        """
        生成路由树

        menus: 总菜单列表
        nodes：节点菜单列表
        name：name拼接，切记Name不能重复
        """
        data = []
        for root in nodes:
            router = schemas.RouterOut.from_orm(root)
            router.name = name + "".join(name.capitalize() for name in router.path.split("/"))
            router.meta = schemas.Meta(title=root.title, icon=root.icon, hidden=root.hidden, alwaysShow=root.alwaysShow)
            if root.menu_type == "0":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_router_tree(menus, sons, router.name)
            data.append(router.dict())
        return data

    def generate_tree_list(self, menus: List[models.VadminMenu], nodes: filter) -> list:
        """
        生成菜单树列表

        menus: 总菜单列表
        nodes：每层节点菜单列表
        """
        data = []
        for root in nodes:
            router = schemas.TreeListOut.from_orm(root)
            if root.menu_type == "0" or root.menu_type == "1":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_tree_list(menus, sons)
            data.append(router.dict())
        return data

    def generate_tree_options(self, menus: List[models.VadminMenu], nodes: filter) -> list:
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
    def menus_order(cls, datas: list, order: str = "order", children: str = "children"):
        """
        菜单排序
        """
        result = sorted(datas, key=lambda menu: menu[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda menu: menu[order])
        return result

