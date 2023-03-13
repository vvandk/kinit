/**
 * 配置浏览器本地存储的方式，可直接存储对象数组。
 * sessionStorage 多标签页情况下互不共享
 * localStorage 多标签页情况下互相共享
 */

import WebStorageCache from 'web-storage-cache'

type CacheType = 'sessionStorage' | 'localStorage'

export const useCache = (type: CacheType = 'localStorage') => {
  const wsCache: WebStorageCache = new WebStorageCache({
    storage: type
  })

  return {
    wsCache
  }
}
