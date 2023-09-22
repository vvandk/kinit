import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import { useStorage } from '@/hooks/web/useStorage'
import { useAppStore } from '@/store/modules/app'
import { useAuthStore } from '@/store/modules/auth'
import qs from 'qs'
import { config } from './config'
import { ElMessage } from 'element-plus'
import request from '@/config/axios'

const { result_code, unauthorized_code, request_timeout } = config

const { getStorage, setStorage } = useStorage()

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: '/api', // api 的 base_url
  timeout: request_timeout, // 请求超时时间
  headers: {} // 请求头信息
})

// request拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const appStore = useAppStore()
    const token = getStorage(appStore.getToken)
    if (token !== '') {
      ;(config.headers as any)['Authorization'] = token // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    if (
      config.method === 'post' &&
      (config.headers as any)['Content-Type'] === 'application/x-www-form-urlencoded'
    ) {
      config.data = qs.stringify(config.data)
    }
    // post put 参数处理
    if (
      (config.method === 'post' || config.method === 'put') &&
      (config.headers as any)['Content-Type'] === 'application/json'
    ) {
      for (const key in config.data) {
        // 参数处理
        if (config.data[key] === '') {
          config.data[key] = null
        }
      }
    }
    // get参数编码
    if (config.method === 'get' && config.params) {
      let url = config.url as string
      url += '?'
      const keys = Object.keys(config.params)
      for (const key of keys) {
        if (
          // 禁止提交的get参数类型
          config.params[key] !== void 0 &&
          config.params[key] !== null &&
          config.params[key] !== ''
        ) {
          url += `${key}=${encodeURIComponent(config.params[key])}&`
        }
      }
      url = url.substring(0, url.length - 1)
      config.params = {}
      config.url = url
    }
    return config
  },
  (error: AxiosError) => {
    // Do something with request error
    console.log('请求报错', error) // for debug
    Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  (response: AxiosResponse<any>) => {
    // 这个状态码是和后端约定好的
    const code = response.data.code || unauthorized_code
    const message = response.data.message || '后端接口无返回内容'
    const refresh = response.headers['if-refresh']

    if (response.config.responseType === 'blob') {
      // 如果是文件流，直接过
      return response
    } else if (code === result_code) {
      if (refresh === '1') {
        // 因token快过期，刷新token
        refreshToken().then((res) => {
          const appStore = useAppStore()
          setStorage(appStore.getToken, `${res.data.token_type} ${res.data.access_token}`)
          setStorage(appStore.getRefreshToken, res.data.refresh_token)
        })
      }
      return response.data
    } else if (code === unauthorized_code) {
      // 因token无效，token过期导致
      refreshToken().then((res) => {
        const appStore = useAppStore()
        setStorage(appStore.getToken, `${res.data.token_type} ${res.data.access_token}`)
        setStorage(appStore.getRefreshToken, res.data.refresh_token)
        ElMessage.error('操作失败，请重试')
      })
    } else {
      ElMessage.error(message)
    }
  },
  (error: AxiosError) => {
    console.log('err', error)
    let { message } = error
    const authStore = useAuthStore()
    const status = error.response?.status
    switch (status) {
      case 400:
        message = '请求错误'
        break
      case 401:
        // 强制要求重新登录，因账号已冻结，账号已过期，手机号码错误，刷新token无效等问题导致
        authStore.logout()
        message = '认证已过期，请重新登录'
        break
      case 403:
        // 强制要求重新登录，因无系统权限，而进入到系统访问等问题导致
        authStore.logout()
        message = '无权限访问，请联系管理员'
        break
      case 404:
        message = `请求地址出错: ${error.response?.config.url}`
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
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// 刷新Token
const refreshToken = (): Promise<IResponse> => {
  const appStore = useAppStore()
  const data = getStorage(appStore.getRefreshToken)
  return request.post({ url: '/auth/token/refresh', data })
}

export { service }
