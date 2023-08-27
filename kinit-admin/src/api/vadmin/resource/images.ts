import request from '@/config/axios'

/**
 * 图片资源管理管理
 */

export const getImagesListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/resource/images', params })
}

export const addImagesApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: '/vadmin/resource/images',
    headersType: 'multipart/form-data',
    data
  })
}

export const delImagesListApi = (data: number[]): Promise<IResponse> => {
  return request.delete({ url: `/vadmin/resource/images`, data })
}

export const getImagesApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/vadmin/resource/images/${dataId}` })
}
