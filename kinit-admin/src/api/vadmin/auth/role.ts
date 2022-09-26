import request from '@/config/axios'

export const getRoleListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/auth/roles/', params })
}
