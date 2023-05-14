import request from '@/common/request/request.js'

// 获取平台中的常见问题类别列表
export function getIssueCategoryList() {
  return request.get('/vadmin/help/issue/categorys/platform/1')
}

// 获取问题详情
export function getIssue(dataId) {
  return request.get(`/vadmin/help/issues/${dataId}`)
}

// 更新常见问题查看次数+1
export function updateIssueAddViewNumber(dataId) {
  return request.get(`/vadmin/help/issues/add/view/number/${dataId}`)
}
