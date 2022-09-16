import { defineStore } from 'pinia'
import { store } from '../index'
import { UserLoginType } from '@/api/login/types'
import { loginApi } from '@/api/login'

export interface AuthState {
  token: string
  is_reset_password: boolean
  user_id: number
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: (): AuthState => ({
    token: '',
    is_reset_password: false,
    user_id: 0
  }),
  persist: {
    // 开启持久化存储
    enabled: true
  },
  getters: {
    getToken(): string {
      return this.token
    },
    getUserId(): number {
      return this.user_id
    },
    getIsResetPassword(): boolean {
      return this.is_reset_password
    }
  },
  actions: {
    async login(formData: UserLoginType) {
      const res = await loginApi(formData)
      if (res) {
        console.log('登录成功', res)
      } else {
        console.log('登录失败', res)
      }
      // this.token = token
      // this.is_reset_password = is_reset_password
      // this.user_id = user_id
      return res
    }
  }
})

export const useAuthStoreWithOut = () => {
  return useAuthStore(store)
}
