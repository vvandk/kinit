import request from '@/config/axios'

// 上传图片到阿里云OSS
export const uploadImageToOSS = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/vadmin/system/upload/image/to/oss`,
    headersType: 'multipart/form-data',
    data
  })
}

// 上传图片到阿里云OSS
export const uploadVideoToOSS = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/vadmin/system/upload/video/to/oss`,
    headersType: 'multipart/form-data',
    data
  })
}

// 上传图片到阿里云OSS
export const uploadFileToOSS = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/vadmin/system/upload/file/to/oss`,
    headersType: 'multipart/form-data',
    data
  })
}
