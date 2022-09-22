import { defineStore } from 'pinia'
import { store } from '../index'
import { UserLoginType } from '@/api/login/types'
import { loginApi } from '@/api/login'

export interface AuthState {
  token: string
  is_reset_password: boolean
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: (): AuthState => ({
    token: '',
    is_reset_password: false
  }),
  persist: {
    // 开启持久化存储
    enabled: true
  },
  getters: {
    getToken(): string {
      return this.token
    },
    getIsResetPassword(): boolean {
      return this.is_reset_password
    }
  },
  actions: {
    async login(formData: UserLoginType) {
      const res = await loginApi(formData)
      if (res) {
        this.token = `${res.data.token_type} ${res.data.access_token}`
        this.is_reset_password = res.data.is_reset_password
      }
      return res
    }
  }
})

export const useAuthStoreWithOut = () => {
  return useAuthStore(store)
}
