#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/10/19 15:41 
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 简要说明

from fastapi import APIRouter, Depends
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from utils.response import SuccessResponse
import datetime
from apps.vadmin.record.crud import LoginRecordDal

app = APIRouter()


###########################################################
#    工作区管理
###########################################################
@app.get("/project", summary="获取项目")
async def get_project():
    data = [
        {
            "name": 'Mysql',
            "icon": 'vscode-icons:file-type-mysql',
            "message": '最流行的关系型数据库管理系统',
            "personal": 'kinit',
            "link": "https://www.mysql.com/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": 'FastAPI',
            "icon": 'simple-icons:fastapi',
            "message": '一个现代、快速(高性能)的 web 框架',
            "personal": 'kinit',
            "link": "https://fastapi.tiangolo.com/zh/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": 'Vue',
            "icon": 'logos:vue',
            "message": '渐进式 JavaScript 框架',
            "personal": 'kinit',
            "link": "https://cn.vuejs.org/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": 'Element-plus',
            "icon": 'logos:element',
            "message": '面向设计师和开发者的组件库',
            "personal": 'kinit',
            "link": "https://element-plus.org/zh-CN/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": 'Typescript',
            "icon": 'vscode-icons:file-type-typescript-official',
            "message": 'TypeScript是JavaScript类型的超集',
            "personal": 'kinit',
            "link": "https://www.typescriptlang.org/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": 'Vite',
            "icon": 'vscode-icons:file-type-vite',
            "message": 'Vite 下一代的前端工具链',
            "personal": 'kinit',
            "link": "https://cn.vitejs.dev/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    ]
    return SuccessResponse(data)


@app.get("/dynamic", summary="获取动态")
async def get_dynamic():
    data = [
        {
            "keys": ['workplace.push', 'Github'],
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "keys": ['workplace.push', 'Github'],
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    ]
    return SuccessResponse(data)


@app.get("/team", summary="获取团队信息")
async def get_team():
    data = [
        {
            "name": 'Mysql',
            "icon": 'vscode-icons:file-type-mysql'
        },
        {
            "name": 'Vue',
            "icon": 'logos:vue'
        },
        {
            "name": 'Element-plus',
            "icon": 'logos:element'
        },
        {
            "name": 'Fastapi',
            "icon": 'simple-icons:fastapi'
        },
        {
            "name": 'Typescript',
            "icon": 'vscode-icons:file-type-typescript-official'
        },
        {
            "name": 'Vite',
            "icon": 'vscode-icons:file-type-vite'
        }
    ]
    return SuccessResponse(data)


@app.get("/shortcuts", summary="获取快捷操作")
async def get_shortcuts():
    data = [
        {
            "name": "前端文档",
            "link": "https://element-plus-admin-doc.cn/"
        },
        {
            "name": "Swagger UI 接口文档",
            "link": "http://kinit.ktianc.top/api/docs"
        },
        {
            "name": "Redoc 接口文档",
            "link": "http://kinit.ktianc.top/api/redoc"
        },
        {
            "name": "Windi CSS 文档",
            "link": "https://cn.windicss.org/guide/"
        },
        {
            "name": "Iconify 文档",
            "link": "https://icon-sets.iconify.design/"
        },
        {
            "name": "echarts 文档",
            "link": "https://echarts.apache.org/zh/index.html"
        },
    ]
    return SuccessResponse(data)
