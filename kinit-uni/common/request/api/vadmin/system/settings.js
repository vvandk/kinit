import request from '@/common/request/request'

// 获取系统基本配置
export function getSystemBaseConfigApi() {
  return request.get('/vadmin/system/settings/base/config')
}
