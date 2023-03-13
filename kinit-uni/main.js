import Vue from 'vue'
import App from './App'
import store from './store' // store
import plugins from './plugins' // plugins
import { router, RouterMount } from './permission.js' // 路由拦截
import uView from 'uview-ui'

Vue.use(uView)
Vue.use(router)
Vue.use(plugins)

// 调用setConfig方法，方法内部会进行对象属性深度合并，可以放心嵌套配置
// 文档：https://www.uviewui.com/components/setting.html
// 配置后，很多组件的默认尺寸就变了，需要手动调整，不熟悉不建议开启
// 需要在Vue.use(uView)之后执行
uni.$u.setConfig({
  // 修改$u.config对象的属性
  config: {
    // 修改默认单位为rpx，相当于执行 uni.$u.config.unit = 'rpx'
    unit: 'rpx'
  },
  // 修改$u.props对象的属性
  props: {
    // 修改radio组件的size参数的默认值，相当于执行 uni.$u.props.radio.size = 30
    radio: {
      size: 33,
      labelSize: 30
    },
    button: {
      loadingSize: 28
    },
    text: {
      size: 30,
      color: '#000'
    }
    // 其他组件属性配置
    // ......
  }
})

Vue.config.productionTip = false
Vue.prototype.$store = store

App.mpType = 'app'

const app = new Vue({
  ...App
})

//v1.3.5起 H5端 你应该去除原有的app.$mount();使用路由自带的渲染方式
// #ifdef H5
RouterMount(app, router, '#app')
// #endif

// #ifndef H5
app.$mount() //为了兼容小程序及app端必须这样写才有效果
// #endif
