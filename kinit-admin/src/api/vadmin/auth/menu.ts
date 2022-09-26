import request from '@/config/axios'

export const getMenuListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/menus/', params })
}
