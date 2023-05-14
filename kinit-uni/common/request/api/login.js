import request from '@/common/request/request.js'

// 登录方法
export function login(telephone, password) {
  const data = {
    telephone,
    password,
    method: '0',
    platform: '1'
  }
  return request.post('/auth/login', data)
}

// 获取用户详细信息
export function getInfo() {
  return request.get('/vadmin/auth/user/admin/current/info')
}

// 更新用户openid
export function setUserOpenid(code) {
  const params = { code }
  return request.put('/vadmin/auth/users/wx/server/openid', {}, { params: params })
}

// 使用微信一键登录
export function wxCodeLogin(code) {
  const data = {
    code,
    method: '2',
    platform: '1'
  }
  return request.post('/auth/wx/login', data)
}
