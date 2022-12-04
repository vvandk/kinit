import request from '@/common/request/request.js'

// 登录方法
export function login(telephone, password, method) {
  const data = {
    telephone,
    password,
	  method,
	  platform: '1'
  }
	return request.post(`/auth/login/`, data)
}

// 获取用户详细信息
export function getInfo() {
	return request.get(`/vadmin/auth/user/current/info/`)
}
