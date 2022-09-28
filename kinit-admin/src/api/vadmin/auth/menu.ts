import request from '@/config/axios'

export const getMenuListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/menus/', params })
}

export const delMenuListApi = (params: any): Promise<IResponse> => {
  return request.delete({ url: '/vadmin/auth/menus/', params })
}

export const getMenuTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/menus/tree/options/' })
}
