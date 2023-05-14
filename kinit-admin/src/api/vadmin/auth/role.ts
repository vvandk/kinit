import request from '@/config/axios'

export const getRoleListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/roles', params })
}

export const addRoleListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/vadmin/auth/roles', data })
}

export const delRoleListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/vadmin/auth/roles', data })
}

export const putRoleListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/vadmin/auth/roles/${data.id}`, data })
}

export const getRoleApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/vadmin/auth/roles/${dataId}` })
}

export const getRoleOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: `/vadmin/auth/roles/options` })
}
