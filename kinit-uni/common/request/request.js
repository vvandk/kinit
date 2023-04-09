import luchRequest from '@/components/luch-request' // 使用npm
import config from '@/config.js'
import errorCode from '@/common/request/errorCode'
import { getToken, getRefreshToken, setToken, setRefreshToken } from '@/common/utils/auth'
import { toast } from '@/common/utils/common'
import store from '@/store'
import request from '@/common/request/request.js'

// luch-request插件官网：https://www.quanzhan.co/luch-request/guide/3.x/#%E5%85%A8%E5%B1%80%E8%AF%B7%E6%B1%82%E9%85%8D%E7%BD%AE
// 创建luchRequest实例
const http = new luchRequest({
  baseURL: config.baseUrl,
  timeout: 20000, // 请求超时时间
  dataType: 'json',
  custom: {
    loading: true
  }
})

// 请求拦截器
http.interceptors.request.use(
  (config) => {
    // 在发送请求之前
    let token = getToken()
    if (token) {
      // 添加头信息，token验证
      config.header['Authorization'] = token
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  (res) => {
    // console.log("响应拦截器：", res)
    // 未设置状态码则默认401状态
    const code = res.data.code || 200
    // 获取错误信息
    const msg = res.data.message || errorCode[code] || errorCode['default']
    // 是否刷新token
    const refresh = res.header['if-refresh']
    if (code === 500) {
      toast(msg)
      return Promise.reject(new Error(msg))
    } else if (code === 401) {
      // 因token快过期，刷新token
      refreshToken().then((res) => {
        setToken(`${res.data.token_type} ${res.data.access_token}`)
        setRefreshToken(res.data.refresh_token)
      })
      toast('操作失败，请重试')
      return Promise.reject('error')
    } else if (code !== 200) {
      toast(msg)
      return Promise.reject('error')
    } else if (code === 200) {
      if (refresh === '1') {
        // 因token快过期，刷新token
        refreshToken().then((res) => {
          setToken(`${res.data.token_type} ${res.data.access_token}`)
          setRefreshToken(res.data.refresh_token)
        })
      }
      return res.data
    } else {
      return res.data
    }
  },
  (error) => {
    console.log('err', error)
    let message = error.data.message || error.errMsg
    const status = error.statusCode
    switch (status) {
      case 400:
        message = '请求错误'
        break
      case 401:
        // 强制要求重新登录，因账号已冻结，账号已过期，手机号码错误，刷新token无效等问题导致
        store.dispatch('auth/LogOut')
        message = '未认证，请登录'
        break
      case 403:
        message = '拒绝访问'
        break
      case 404:
        message = '请求地址出错'
        break
      case 408:
        message = '请求超时'
        break
      case 500:
        message = '服务器内部错误'
        break
      case 501:
        message = '服务未实现'
        break
      case 502:
        message = '网关错误'
        break
      case 503:
        message = '服务不可用'
        break
      case 504:
        message = '网关超时'
        break
      case 505:
        message = 'HTTP版本不受支持'
        break
      default:
        break
    }
    toast(message)
    return Promise.reject(error)
  }
)

// 刷新 token
function refreshToken() {
  const data = JSON.stringify(getRefreshToken())
  return request.post('/auth/token/refresh/', data)
}

export default http
