import request from '@/config/axios'

export const getUserListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/users/', params })
}

export const addUserListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/vadmin/auth/users/', data })
}

export const delUserListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/vadmin/auth/users/', data })
}

export const putUserListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/vadmin/auth/users/${data.id}/`, data })
}

export const getUserApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/vadmin/auth/users/${dataId}/` })
}
