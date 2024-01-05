import request from '@/config/axios'

export const getDeptListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/depts', params })
}

export const delDeptListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/vadmin/auth/depts', data })
}

export const addDeptListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/vadmin/auth/depts', data })
}

export const putDeptListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/vadmin/auth/depts/${data.id}`, data })
}

export const getDeptTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/dept/tree/options' })
}

export const getDeptUserTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/dept/user/tree/options' })
}
