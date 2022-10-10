import { defineStore } from 'pinia'
import { store } from '../index'
import { UserLoginType } from '@/api/login/types'
import { loginApi } from '@/api/login'
import { useAppStore } from '@/store/modules/app'
import { useCache } from '@/hooks/web/useCache'
import { getCurrentUserInfo } from '@/api/vadmin/auth/user'
import { resetRouter } from '@/router'
import { useTagsViewStore } from '@/store/modules/tagsView'

const appStore = useAppStore()
const { wsCache } = useCache()
const tagsViewStore = useTagsViewStore()

export interface UserState {
  id?: number
  telephone?: string
  name?: string
  nickname?: string
  avatar?: string
  gender?: string
  roles?: Recordable[]
  create_datetime?: string
}

export interface AuthState {
  user: UserState
  isUser: boolean
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: (): AuthState => {
    return {
      user: {},
      isUser: false
    }
  },
  persist: {
    // 开启持久化存储
    enabled: true
  },
  getters: {
    getUser(): UserState {
      return this.user
    },
    getIsUser(): boolean {
      return this.isUser
    }
  },
  actions: {
    async login(formData: UserLoginType) {
      const res = await loginApi(formData)
      if (res) {
        wsCache.set(appStore.getToken, `${res.data.token_type} ${res.data.access_token}`)
        // 存储用户信息
        wsCache.set(appStore.getUserInfo, res.data.user)
        this.user = res.data.user
        this.isUser = true
      }
      return res
    },
    logout() {
      wsCache.clear()
      this.user = {}
      this.isUser = false
      resetRouter()
      tagsViewStore.delAllViews()
    },
    updateUser(data: UserState) {
      this.user.gender = data.gender
      this.user.name = data.name
      this.user.nickname = data.nickname
      wsCache.set(appStore.getUserInfo, this.user)
    },
    async getUserInfo() {
      const res = await getCurrentUserInfo()
      wsCache.set(appStore.getUserInfo, res.data)
      this.isUser = true
      this.user = res.data
    }
  }
})

export const useAuthStoreWithOut = () => {
  return useAuthStore(store)
}
