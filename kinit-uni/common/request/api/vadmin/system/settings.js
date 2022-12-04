import request from '@/common/request/request'

// 获取系统配置分类
export function getSystemSettingsClassifysApi(params) {
	return request.get(`/vadmin/system/settings/classifys/`, {params: params})
}