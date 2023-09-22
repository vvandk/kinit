import request from '@/config/axios'

export const getMenuListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/menus', params })
}

export const delMenuListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/vadmin/auth/menus', data })
}

export const addMenuListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/vadmin/auth/menus', data })
}

export const putMenuListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/vadmin/auth/menus/${data.id}`, data })
}

export const getMenuTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/menus/tree/options' })
}

export const getMenuRoleTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/menus/role/tree/options' })
}
