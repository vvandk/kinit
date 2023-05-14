import request from '@/common/request/request'

// 更新当前用户基本信息
export function updateCurrentUser(data) {
  return request.post('/vadmin/auth/user/current/update/info', data)
}

// 重置当前用户密码
export function postCurrentUserResetPassword(data) {
  return request.post('/vadmin/auth/user/current/reset/password', data)
}

// 更新当前用户头像
export function postCurrentUserUploadAvatar(filePath) {
  return request.upload('/vadmin/auth/user/current/update/avatar', {
    filePath: filePath,
    name: 'file'
  })
}
