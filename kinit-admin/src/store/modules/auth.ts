import { defineStore } from 'pinia'
import { store } from '../index'
import { UserLoginType } from '@/api/login/types'
import { loginApi } from '@/api/login'
import { useAppStore } from '@/store/modules/app'
import { useCache } from '@/hooks/web/useCache'
import { getCurrentAdminUserInfo } from '@/api/vadmin/auth/user'
import { resetRouter } from '@/router'
import { useTagsViewStore } from '@/store/modules/tagsView'
import router from '@/router'

const { wsCache } = useCache()

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

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => {
    return {
      user: {},
      isUser: false
    }
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
      formData.platform = '0'
      const res = await loginApi(formData)
      if (res) {
        const appStore = useAppStore()
        wsCache.set(appStore.getToken, `${res.data.token_type} ${res.data.access_token}`)
        wsCache.set(appStore.getRefreshToken, res.data.refresh_token)
        // 存储用户信息
        const auth = useAuthStore()
        await auth.getUserInfo()
      }
      return res
    },
    logout() {
      wsCache.clear()
      this.user = {}
      this.isUser = false
      const tagsViewStore = useTagsViewStore()
      tagsViewStore.delAllViews()
      resetRouter()
      router.push('/login')
    },
    updateUser(data: UserState) {
      this.user.gender = data.gender
      this.user.name = data.name
      this.user.nickname = data.nickname
      this.user.telephone = data.telephone
      const appStore = useAppStore()
      wsCache.set(appStore.getUserInfo, this.user)
    },
    async getUserInfo() {
      const res = await getCurrentAdminUserInfo()
      const appStore = useAppStore()
      wsCache.set(appStore.getUserInfo, res.data)
      this.isUser = true
      this.user = res.data
    }
  }
})

export const useAuthStoreWithOut = () => {
  return useAuthStore(store)
}
