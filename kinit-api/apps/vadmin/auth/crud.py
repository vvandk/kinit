#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/2/24 10:21 
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 增删改查
from typing import List

from sqlalchemy import select
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
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
        obj = await super(UserDal, self).create_data(data.dict(exclude={"role_ids"}), True, options, schema)
        for data_id in data.role_ids:
            obj.roles.append(await RoleDal(db=self.db).get_data(data_id=data_id))
        if options:
            obj = await self.get_data(obj.id, options=options)
        if return_obj:
            return obj
        if schema:
            return schema.from_orm(obj).dict()
        return self.out_dict(obj)


class RoleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RoleDal, self).__init__(db, models.VadminRole, schemas.RoleSimpleOut)

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

    async def get_tree_list(self):
        """
        获取菜单树列表
        """
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        menus = queryset.scalars().all()
        roots = filter(lambda i: not i.parent_id, menus)
        return self.generate_tree_list(menus, roots)

    async def get_routers(self, user: models.VadminUser):
        """
        获取路由表
        export interface Menu {
          name: string;   //  菜单名
          icon?: string;  // 菜单图标,如果没有，则会尝试使用route.meta.icon
          path: string;  // 菜单路径
          disabled?: boolean;  // 是否禁用
          children?: Menu[];  // 子菜单
          tag: {  // 菜单标签设置
            dot: boolean;       // 为true则显示小圆点
            content: string';  // 内容
            type: 'error' | 'primary' | 'warn' | 'success';  // 类型
          };
          hideMenu?: boolean;  // 是否隐藏菜单
        }
        """
        if any([i.is_admin for i in user.roles]):
            sql = select(self.model).where(self.model.disabled == False, self.model.menu_type != "2")
            queryset = await self.db.execute(sql)
            menus = queryset.scalars().all()
        else:
            menus = set()
            for role in user.roles:
                role_obj = await RoleDal(self.db).get_data(role.id, options=[models.VadminRole.menus])
                for menu in role_obj.menus:
                    if not menu.disabled and menu.menu_type != "2":
                        menus.add(menu)
        roots = filter(lambda i: not i.parent_id, menus)
        return self.generate_router_tree(menus, roots)

    async def get_treeselect(self):
        """获取菜单树列表信息"""
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.TreeselectOut.from_orm(i).dict() for i in queryset.scalars().all()]

    def generate_router_tree(self, menus: List[models.VadminMenu], nodes: filter) -> list:
        """
        生成路由数

        menus: 总菜单列表
        nodes：节点菜单列表
        """
        data = []
        for root in nodes:
            router = schemas.RouterOut.from_orm(root)
            router.name = router.path.split("/")[-1].capitalize()
            router.meta = schemas.Meta(title=root.title, icon=root.icon)
            if root.menu_type == "0":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_router_tree(menus, sons)
            data.append(router.dict())
        return data

    def generate_tree_list(self, menus: List[models.VadminMenu], nodes: filter) -> list:
        """
        生成菜单树

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




