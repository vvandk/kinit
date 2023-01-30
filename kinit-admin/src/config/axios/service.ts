import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import { useCache } from '@/hooks/web/useCache'
import qs from 'qs'
import { config } from './config'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/modules/auth'

const { result_code, unauthorized_code, request_timeout, token } = config

const { wsCache } = useCache()

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: '/api', // api 的 base_url
  timeout: request_timeout, // 请求超时时间
  headers: {} // 请求头信息
})

// request拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const _token = wsCache.get(token)
    if (_token !== '') {
      ;(config.headers as any)['Authorization'] = _token // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    if (
      config.method === 'post' &&
      (config.headers as any)['Content-Type'] === 'application/x-www-form-urlencoded'
    ) {
      config.data = qs.stringify(config.data)
    }
    // get参数编码
    if (config.method === 'get' && config.params) {
      let url = config.url as string
      url += '?'
      const keys = Object.keys(config.params)
      for (const key of keys) {
        if (config.params[key] !== void 0 && config.params[key] !== null) {
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
    if (response.config.responseType === 'blob') {
      // 如果是文件流，直接过
      return response
    } else if (response.data.code === result_code) {
      return response.data
    } else if (response.data.code === unauthorized_code) {
      // 请重新登录
      ElMessage.error(response.data.message)
      const authStore = useAuthStore()
      authStore.logout()
    } else {
      ElMessage.error(response.data.message)
    }
  },
  (error: AxiosError) => {
    console.log('err' + error)
    let { message } = error
    if (message == 'Network Error') {
      message = '系统接口连接异常'
    } else if (message.includes('timeout')) {
      message = '系统接口请求超时'
    } else if (message.includes('Request failed with status code')) {
      message = '系统接口状态码异常'
    }
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export { service }
