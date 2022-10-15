#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/2/24 10:21 
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 增删改查
from typing import List
from core.exception import CustomException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession

from utils.tools import test_password
from . import models, schemas
from application import settings


class UserDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(UserDal, self).__init__(db, models.VadminUser, schemas.UserSimpleOut)

    async def create_data(self, data: schemas.UserIn, return_obj: bool = False, options: list = None, schema=None):
        """
        创建用户
        """
        password = data.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
        data.password = self.model.get_password_hash(password)
        obj = self.model(**data.dict(exclude={'role_ids'}))
        for data_id in data.role_ids:
            obj.roles.append(await RoleDal(db=self.db).get_data(data_id=data_id))
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
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
        self.db.add(user)
        await self.db.flush()
        return True

    async def update_current_info(self, user: models.VadminUser, data: schemas.UserUpdate):
        """
        更新当前用户信息
        """
        user.name = data.name
        user.nickname = data.nickname
        user.gender = data.gender
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return self.out_dict(user)


class RoleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RoleDal, self).__init__(db, models.VadminRole, schemas.RoleSimpleOut)

    async def create_data(self, data: schemas.RoleIn, return_obj: bool = False, options: list = None, schema=None):
        """创建数据"""
        obj = self.model(**data.dict(exclude={'menu_ids'}))
        for data_id in data.menu_ids:
            obj.menus.append(await MenuDal(db=self.db).get_data(data_id=data_id))
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
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
            sql = select(self.model).where(self.model.disabled == 0, self.model.menu_type != "2")
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

    def generate_router_tree(self, menus: List[models.VadminMenu], nodes: filter) -> list:
        """
        生成路由树

        menus: 总菜单列表
        nodes：节点菜单列表
        """
        data = []
        for root in nodes:
            router = schemas.RouterOut.from_orm(root)
            router.name = router.path.split("/")[-1].capitalize()
            router.meta = schemas.Meta(title=root.title, icon=root.icon, hidden=root.hidden)
            if root.menu_type == "0":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_router_tree(menus, sons)
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
            router = {"value": root.id, "label": root.title}
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

