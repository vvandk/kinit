import { defineStore } from 'pinia'
import { store } from '../index'
import { UserLoginType } from '@/api/login/types'
import { loginApi } from '@/api/login'
import { useStorage } from '@/hooks/web/useStorage'
import { getCurrentAdminUserInfo } from '@/api/vadmin/auth/user'
import { resetRouter } from '@/router'
import { useTagsViewStore } from '@/store/modules/tagsView'
import router from '@/router'
import { ElMessage } from 'element-plus'

const { clear } = useStorage()

export interface UserState {
  id?: number
  telephone?: string
  email?: string
  name?: string
  nickname?: string
  avatar?: string
  gender?: string
  roles?: Recordable[]
  create_datetime?: string
  is_reset_password?: boolean
  last_login?: string
  last_ip?: string
}

export interface AuthState {
  user: UserState // 当前用户基本信息
  isUser: boolean // 是否已经登录并获取到用户信息
  roles: string[] // 当前用户角色 role_key 列表
  permissions: string[] // 当前用户权限列表
  tokenKey: string // 提交认证请求时，设置的 header key
  token: string // 认证 token
  refreshToken: string // 刷新 token
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => {
    return {
      user: {},
      roles: [],
      permissions: [],
      isUser: false,
      tokenKey: 'Authorization',
      token: '',
      refreshToken: ''
    }
  },
  getters: {
    getTokenKey(): string {
      return this.tokenKey
    },
    getToken(): string {
      return this.token
    },
    getRefreshToken(): string {
      return this.refreshToken
    },
    getUser(): UserState {
      return this.user
    },
    getRoles(): string[] {
      return this.roles
    },
    getPermissions(): string[] {
      return this.permissions
    },
    getIsUser(): boolean {
      return this.isUser
    }
  },
  actions: {
    setToken(token: string) {
      this.token = token
    },
    setRefreshToken(refreshToken: string) {
      this.refreshToken = refreshToken
    },
    async login(formData: UserLoginType) {
      formData.platform = '0'
      const res = await loginApi(formData)
      if (res) {
        this.token = `${res.data.token_type} ${res.data.access_token}`
        this.refreshToken = res.data.refresh_token
        // 获取当前登录用户的信息
        await this.setUserInfo()
      }
      return res
    },
    reset() {
      this.user = {}
      this.roles = []
      this.permissions = []
      this.isUser = false
      this.token = ''
      this.refreshToken = ''
    },
    logout(message?: string) {
      clear()
      this.reset()
      const tagsViewStore = useTagsViewStore()
      tagsViewStore.delAllViews()
      resetRouter()
      router.push('/login')
      if (message) {
        ElMessage.error(message)
      }
    },
    // 这里更新用户是自己在个人中心更新自己的用户信息，不包括在用户列表中更新的，所以不包含权限角色等信息
    // 用户信息取消使用持久化存储，仅使用共享存储
    updateUser(data: UserState) {
      this.user.gender = data.gender
      this.user.name = data.name
      this.user.nickname = data.nickname
      this.user.telephone = data.telephone
    },
    // 获取用户详细信息，包括角色，权限
    // 用户信息取消使用持久化存储，仅使用共享存储
    async setUserInfo() {
      const res = await getCurrentAdminUserInfo()
      this.isUser = true
      this.user = res.data
      this.roles = res.data.roles.map((item) => {
        if (!item.disabled) {
          return item.role_key
        }
      })
      this.permissions = res.data.permissions
    }
  },
  persist: true
})

export const useAuthStoreWithOut = () => {
  return useAuthStore(store)
}
