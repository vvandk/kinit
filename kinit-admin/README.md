# vue-element-plus-admin

vue-element-plus-admin 是一个基于 `element-plus` 免费开源的中后台模版。使用了最新的`vue3`，`vite3`，`TypeScript`等主流技术开发，开箱即用的中后台前端解决方案，可以用来作为项目的启动模版，也可用于学习参考。并且时刻关注着最新技术动向，尽可能的第一时间更新。

vue-element-plus-admin 的定位是后台集成方案，不太适合当基础模板来进行二次开发。因为集成了很多你可能用不到的功能，会造成不少的代码冗余。如果你的项目不关注这方面的问题，也可以直接基于它进行二次开发。

如需要基础模版，请切换到 `tempalte` 分支，`tempalte` 只简单集成了一些如：布局、动态菜单等常用布局功能，更适合开发者进行二次开发。

## 特性

- **最新技术栈**：使用 Vue3/vite3 等前端前沿技术开发
- **TypeScript**: 应用程序级 JavaScript 的语言
- **主题**: 可配置的主题
- **国际化**：内置完善的国际化方案
- **自定义数据** 内置 Mock 数据方案
- **权限** 内置完善的动态路由权限生成方案
- **组件** 二次封装了多个常用的组件
- **示例** 内置丰富的示例

## 预览

- [vue-element-plus-admin](https://element-plus-admin.cn/) - 完整版 github 站点
- [vue-element-plus-admin](https://kailong110120130.gitee.io/vue-element-plus-admin) - 完整版 gitee 站点

帐号：**admin/admin test/test**

`admin` 帐号用于模拟服务端控制权限，服务端返回什么就渲染什么

`test` 帐号用于模拟前端控制权限，服务端只返回需要显示的菜单 key，前端进行匹配渲染

## 文档

[文档地址 Github](https://element-plus-admin-doc.cn/)

[文档地址 Gitee](https://kailong110120130.gitee.io/vue-element-plus-admin-doc)

## 前序准备

- [node](http://nodejs.org/) 和 [git](https://git-scm.com/) - 项目开发环境
- [Vite](https://vitejs.dev/) - 熟悉 vite 特性
- [Vue3](https://v3.vuejs.org/) - 熟悉 Vue 基础语法
- [TypeScript](https://www.typescriptlang.org/) - 熟悉 `TypeScript` 基本语法
- [Es6+](http://es6.ruanyifeng.com/) - 熟悉 es6 基本语法
- [Vue-Router-Next](https://next.router.vuejs.org/) - 熟悉 vue-router 基本使用
- [Element-Plus](https://element-plus.org/) - element-plus 基本使用
- [Mock.js](https://github.com/nuysoft/Mock) - mockjs 基本语法

## 安装和使用

- 获取代码

```bash
git clone https://github.com/kailong321200875/vue-element-plus-admin.git
```

- 安装依赖

```bash
cd vue-element-plus-admin

pnpm install
```

- 运行

```bash
pnpm run dev
```

- 打包

```bash
pnpm run build:pro
```

## 更新日志

[更新日志](./CHANGELOG.md)