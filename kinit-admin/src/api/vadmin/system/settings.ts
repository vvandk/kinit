import request from '@/config/axios'

export const getSystemSettingsTabsApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/vadmin/system/settings/tabs', data })
}

export const getSystemSettingsApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/tabs/values', params })
}

export const putSystemSettingsApi = (data: any): Promise<IResponse> => {
  return request.put({ url: '/vadmin/system/settings/tabs/values', data })
}

// 获取系统基础配置，每次进入系统时使用
export const getSystemBaseConfigApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/base/config' })
}

// 获取系统隐私协议
export const getSystemPrivacyApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/privacy' })
}

// 获取系统用户协议
export const getSystemAgreementApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/agreement' })
}
