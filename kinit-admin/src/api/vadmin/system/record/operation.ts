import request from '@/config/axios'

export const getRecordOperationListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/record/operations', params })
}
