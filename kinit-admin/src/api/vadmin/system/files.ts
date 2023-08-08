import request from '@/config/axios'

// 上传图片到阿里云OSS
export const uploadImageToOSSApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/vadmin/system/upload/image/to/oss`,
    headersType: 'multipart/form-data',
    data
  })
}

// 上传图片到阿里云OSS
export const uploadVideoToOSSApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/vadmin/system/upload/video/to/oss`,
    headersType: 'multipart/form-data',
    data
  })
}

// 上传图片到阿里云OSS
export const uploadFileToOSSApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/vadmin/system/upload/file/to/oss`,
    headersType: 'multipart/form-data',
    data
  })
}
