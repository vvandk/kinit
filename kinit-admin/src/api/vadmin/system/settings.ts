import request from '@/config/axios'

export const getSystemSettingsTabsApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/tabs/', params })
}

export const getSystemSettingsApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/tabs/values/', params })
}

export const putSystemSettingsApi = (data: any): Promise<IResponse> => {
  return request.put({ url: '/vadmin/system/settings/tabs/values/', data })
}

export const getSystemSettingsClassifysApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/classifys/', params })
}

export const getSystemSettingsConfigValueApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/settings/config/value/', params })
}
