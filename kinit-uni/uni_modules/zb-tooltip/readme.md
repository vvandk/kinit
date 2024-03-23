## 介绍
基于uni-app开发的一个普通的提示组件，功能点击提示


## 友情链接
#### vue-admin-perfect —— [企业级、通用型中后台前端解决方案 预览地址](http://182.61.5.190:8889/)
#### vue-admin-perfect —— [企业级、通用型中后台前端解决方案（基于vue3.0+TS+Element-Plus  最新版，同时支持电脑，手机，平板)](https://github.com/zouzhibin/vue-admin-perfect)


## Tooltip 属性
| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| ------ | ------ | ------ | ------ | ------ |
| visible | 是否显示 tooltip，支持 .sync 修饰符 | Boolean |visible.sync | false |
| content | 显示的内容，也可以通过 slot#content | String |-- | ' ' |
| color | 自定义主题颜色| String |'#303133' | '#303133' |
| placement | Tooltip 的出现位置 | String |top/top-start/top-end/bottom/bottom-start/bottom-end/left/left-start/left-end/right/right-start/right-end | top |


## Slot 插槽
| 参数 | 说明 |
| ------ | ------ |
| content | 显示提示框得内容 |


```
因为uniapp 中小程序中没有window对象，需手动调用 关闭
 第一种办法关闭：this.$refs.tooltip.close()
 第二种办法关闭：visible.sync = false

```
