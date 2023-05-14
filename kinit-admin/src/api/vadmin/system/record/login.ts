import request from '@/config/axios'

export const getRecordLoginListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/record/logins', params })
}
