//vue.config.js
const TransformPages = require('uni-read-pages')
const { webpack } = new TransformPages()

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        ROUTES: webpack.DefinePlugin.runtimeValue(() => {
          const tfPages = new TransformPages({
            // includes 中包含的是router会读取pages路由中的字段名
            // 后续如果有用到meta等路由信息，可以在 includes 里增加 'meta'，
            // 在pages路由中写对应的数据，router中就可以获取得到
            includes: ['path', 'name', 'aliasPath', 'meta']
          })
          return JSON.stringify(tfPages.routes)
        }, true)
      })
    ]
  },
  devServer: {
    port: 8080,
    https: false,
    disableHostCheck: true // 禁止访问本地host文件
  }
}
