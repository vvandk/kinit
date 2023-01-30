import { defineStore } from 'pinia'
import { store } from '../index'
import { UserLoginType } from '@/api/login/types'
import { loginApi } from '@/api/login'
import { useCache } from '@/hooks/web/useCache'
import { getCurrentUserInfo } from '@/api/vadmin/auth/user'
import { resetRouter } from '@/router'
import { config } from '@/config/axios/config'
import { useTagsViewStore } from '@/store/modules/tagsView'

const { token } = config

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
  userInfo: string
  user: UserState
  isUser: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => {
    return {
      userInfo: 'userInfo', // 登录信息存储字段-建议每个项目换一个字段，避免与其他项目冲突
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
    },
    getUserInfo(): string {
      return this.userInfo
    }
  },
  actions: {
    async login(formData: UserLoginType) {
      formData.platform = '0'
      const res = await loginApi(formData)
      if (res) {
        wsCache.set(token, `${res.data.token_type} ${res.data.access_token}`)
        // 存储用户信息
        await this.getUserInfoAction()
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
      window.location.href = '/login'
    },
    updateUser(data: UserState) {
      this.user.gender = data.gender
      this.user.name = data.name
      this.user.nickname = data.nickname
      this.user.telephone = data.telephone
      wsCache.set(this.userInfo, this.user)
    },
    async getUserInfoAction() {
      const res = await getCurrentUserInfo()
      wsCache.set(this.userInfo, res.data)
      this.isUser = true
      this.user = res.data
    }
  }
})

export const useAuthStoreWithOut = () => {
  return useAuthStore(store)
}
