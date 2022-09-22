import { defineStore } from 'pinia'
import { store } from '../index'
import { UserLoginType } from '@/api/login/types'
import { loginApi } from '@/api/login'
import { useAppStore } from '@/store/modules/app'
import { useCache } from '@/hooks/web/useCache'

const appStore = useAppStore()
const { wsCache } = useCache()

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => {
    return {}
  },
  persist: {
    // 开启持久化存储
    enabled: true,
    strategies: [
      {
        key: 'authStore',
        storage: localStorage
      }
    ]
  },
  getters: {},
  actions: {
    async login(formData: UserLoginType) {
      const res = await loginApi(formData)
      if (res) {
        wsCache.set(appStore.getToken, `${res.data.token_type} ${res.data.access_token}`)
        // 存储用户信息
        wsCache.set(appStore.getUserInfo, res.data.user)
      }
      return res
    }
  }
})

export const useAuthStoreWithOut = () => {
  return useAuthStore(store)
}
