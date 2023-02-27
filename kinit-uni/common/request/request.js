import luchRequest from '@/components/luch-request' // 使用npm
import config from '@/config.js';
import errorCode from "@/common/request/errorCode";
import { getToken } from '@/common/utils/auth'
import { toast, showConfirm } from '@/common/utils/common'
import store from '@/store'

// luch-request插件官网：https://www.quanzhan.co/luch-request/guide/3.x/#%E5%85%A8%E5%B1%80%E8%AF%B7%E6%B1%82%E9%85%8D%E7%BD%AE
// 创建luchRequest实例
console.log(config.baseUrl)
const http = new luchRequest({
  baseURL: config.baseUrl,
  timeout: 20000, // 请求超时时间
  dataType: 'json',
  custom: {
  	loading: true
  },
  sslVerify: true,
  header: {}
})


// 请求拦截器
http.interceptors.request.use(
  config => {
    // 在发送请求之前
  	let token = getToken()
  	if (token) {
  	  // 添加头信息，token验证
  	  config.header["Authorization"] = token
  	}
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(res => {
	  // console.log("响应拦截器：", res)
	  // 未设置状态码则默认成功状态
	  const code = res.data.code || 200;
	  // 获取错误信息
	  const msg = res.data.message || errorCode[code] || errorCode["default"];
	  if (code === 500) {
	  	toast(msg)
		  return Promise.reject(new Error(msg));
	  } else if (code === 401) {
			showConfirm("登录状态已过期，您可以继续留在该页面，或者重新登录?").then(res => {
			  if (res.confirm) {
			    store.dispatch('auth/LogOut')
			  }
			})
			return Promise.reject("error");
		} else if (code !== 200) {
		  toast(msg)
		  return Promise.reject("error");
	  } else {
		  return res.data;
	  }
	},
	error => {
	  console.log("请求状态码服务器直接报错", error);
	  let { errMsg } = error;
	  if (errMsg == "request:fail") {
		  errMsg = "接口连接异常";
	  } else if (errMsg == "request:fail timeout") {
		  errMsg = "接口连接超时";
	  } else {
		  errMsg = error.data.message;
	  }
	  toast(errMsg)
	  return Promise.reject(error);
	}
);

export default http