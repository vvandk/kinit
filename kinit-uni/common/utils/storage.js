import { auth } from './constant'

// 主要用于缓存store中数据使用！！！！！
// 更加方便管理缓存，可以实现一键清除固定的缓存

// 存储变量名
let storageKey = 'storage_data'

// 存储节点变量名，只存储包含的变量名，不包含的不处理
let storageNodeKeys = [...Object.values(auth)]

// 存储的数据
let storageData = uni.getStorageSync(storageKey) || {}

const storage = {
  set: function (key, value) {
    if (storageNodeKeys.indexOf(key) != -1) {
      let tmp = uni.getStorageSync(storageKey)
      tmp = tmp ? tmp : {}
      tmp[key] = value
      uni.setStorageSync(storageKey, tmp)
    }
  },
  get: function (key) {
    return storageData[key] || ''
  },
  remove: function (key) {
    delete storageData[key]
    uni.setStorageSync(storageKey, storageData)
  },
  clean: function () {
    uni.removeStorageSync(storageKey)
  }
}

export default storage
