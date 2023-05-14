import request from '@/common/request/request.js'

// 获取多个字典类型下的字典元素列表
export function getDictTypeDetailsApi(data) {
  return request.post('/vadmin/system/dict/types/details', data)
}
