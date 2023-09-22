
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

![image-20221201101340689](..\images\uni\image-20221201101340689.png)

uView UI，是[uni-app](https://uniapp.dcloud.io/)全面兼容nvue的uni-app生态框架，全面的组件和便捷的工具会让您信手拈来，如鱼得水

## 开发工具

在此项目中我将开发`uni-app`的开发工具从 Hbuilder X 换到了 VSCode，没有谁好谁坏，只是本人更习惯使用 VSCode，但是在运行项目时依然使用的是 Hbuilder X，VSCode只是用来编写代码。当然使用 Hbuilder X 也是支持的，只做一个分享。

以下是我在VSCode中安装的几个插件：

1. 名称: Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code
2. 名称: ESLint
3. 名称: Image preview
4. 名称: Markdown Preview Enhanced
5. 名称: Path Intellisense
6. 名称: Prettier - Code formatter
7. 名称: Sass (.sass only)
8. 名称: SCSS IntelliSense
9. 名称: Stylelint
10. 名称: uni-app-schemas
11. 名称: uni-app-snippets
12. 名称: uni-create-view
13. 名称: Vetur

## 演示图

<table>
    <tr>
        <td><img src="https://oscimg.oschina.net/oscnet/up-3ea20e447ac621a161e395fb53ccc683d84.png"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/up-a6f23cf9a371a30165e135eff6d9ae89a9d.png"/></td>
		<td><img src="https://oscimg.oschina.net/oscnet/up-ff5f62016bf6624c1ff27eee57499dccd44.png"/></td>
    </tr>
	<tr>
        <td><img src="https://oscimg.oschina.net/oscnet/up-b9a582fdb26ec69d407fabd044d2c8494df.png"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/up-96427ee08fca29d77934cfc8d1b1a637cef.png"/></td>
		<td><img src="https://oscimg.oschina.net/oscnet/up-5fdadc582d24cccd7727030d397b63185a3.png"/></td>
    </tr>
	<tr>
        <td><img src="https://oscimg.oschina.net/oscnet/up-0a36797b6bcc50c36d40c3c782665b89efc.png"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/up-d77995cc00687cedd00d5ac7d68a07ea276.png"/></td>
		<td><img src="https://oscimg.oschina.net/oscnet/up-fa8f5ab20becf59b4b38c1b92a9989e7109.png"/></td>
    </tr>
</table>
