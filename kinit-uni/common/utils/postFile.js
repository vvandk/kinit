/**
 uniapp 上传文件到后台接口
 
 官方文档：https://uniapp.dcloud.io/api/request/network-file.html#uploadfile
 博客：https://www.jianshu.com/p/71ad2f45120c
 */


import { API_BASE_URL } from '@/common/setting/index'
import { getToken, removeToken, getStorage } from '@/common/utils/cookies'


// 单个文件上传
export function uploadFile(api, file, data={}) {
  return new Promise((resolve, reject) => {
	  uni.uploadFile({
		  url: API_BASE_URL + api,
		  filePath: file,
		  name: 'file',
		  timeout: 60000,
		  formData: data,
		  header: {
			  ossign: getStorage("ossign"),
			  Authorization: getToken()
		  },
		  success: (res) => {
			  let data = JSON.parse(res.data);
			  if (data.code !== 200) {
				  reject(data);
			  }
			  resolve(data);
		  },
		  fail: (err) => {
			  console.log("上传失败", err);
			  reject(err);
		  }
	  });
  })
}
