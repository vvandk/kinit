import request from '@/config/axios'

export const addFilesListApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/vadmin/system/files/`,
    headersType: 'multipart/form-data',
    data
  })
}
