
## 若依平台简介

RuoYi App 移动解决方案，采用uniapp框架，一份代码多终端适配，同时支持APP、小程序、H5！实现了与[RuoYi-Vue](https://gitee.com/y_project/RuoYi-Vue)、[RuoYi-Cloud](https://gitee.com/y_project/RuoYi-Cloud)完美对接的移动解决方案！目前已经实现登录、我的、工作台、编辑资料、头像修改、密码修改、常见问题、关于我们等基础功能。

* 应用框架基于[uniapp](https://uniapp.dcloud.net.cn/)，支持小程序、H5、Android和IOS。
* 前端组件加入了[uni-ui](https://github.com/dcloudio/uni-ui)，全端兼容的高性能UI框架。


## 若依技术文档

- 官网网站：[http://ruoyi.vip](http://ruoyi.vip)
- 文档地址：[http://doc.ruoyi.vip](http://doc.ruoyi.vip)
- H5页体验：[http://h5.ruoyi.vip](http://h5.ruoyi.vip)
- 小程序体验

<img src="https://oscimg.oschina.net/oscnet/up-26c76dc90b92acdbd9ac8cd5252f07c8ad9.jpg" alt="小程序演示"/>

## 二次开发

是的，KINIT-UNI 是在若依-移动端的基础上进行的二次开发，在此感谢若依团队！

二次开发中我们重新将接口请求改为了使用 `luch-request`，项目结构也有所改动，并且加入了 `uView UI` 组件，`uni-simple-router` 路由拦截。



开发环境：HBuilder X

## 依赖插件

- [uni-read-pages](https://github.com/SilurianYang/uni-read-pages) ：自动读取 `pages.json` 所有配置。
- [uni-simple-router](https://hhyang.cn/v2/start/quickstart.html) ：在uni-app中使用vue-router的方式进行跳转路由，路由拦截。

## 依赖组件

### color UI

- 文档地址：http://docs.xzeu.com/
- 源码地址：https://github.com/weilanwl/coloruicss
- 微信小程序：#小程序://ColorUI组件库/0YmCxm5PUBuChYJ

该项目已在 2019 年停止维护，但因若依组件中有多处使用，所以在这里不做移除，新加入uView UI框架，两者不冲突

### uView UI

- 源码地址：https://github.com/umicro/uView2.0
- 文档地址：https://uviewui.com

uView UI，是[uni-app](https://uniapp.dcloud.io/)全面兼容nvue的uni-app生态框架，全面的组件和便捷的工具会让您信手拈来，如鱼得水
