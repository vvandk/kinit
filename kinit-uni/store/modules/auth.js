import storage from '@/common/utils/storage'
import constant from '@/common/utils/constant'
import { login, getInfo } from '@/common/request/api/login'
import { getToken, setToken, removeToken } from '@/common/utils/auth'

const auth = {
  state: {
    token: getToken(),
		isUser: storage.get(constant.isUser) || false,
    name: storage.get(constant.name),
    nickname: storage.get(constant.nickname),
    telephone: storage.get(constant.telephone),
    avatar: storage.get(constant.avatar),
    createDatetime: storage.get(constant.createDatetime),
    roles: storage.get(constant.roles),
    permissions: storage.get(constant.permissions)
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, name) => {
      state.name = name
      storage.set(constant.name, name)
    },
		SET_NICKNAME: (state, nickname) => {
		  state.nickname = nickname
		  storage.set(constant.nickname, nickname)
		},
		SET_CREATE_DATETIME: (state, createDatetime) => {
		  state.createDatetime = createDatetime
		  storage.set(constant.createDatetime, createDatetime)
		},
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
      storage.set(constant.avatar, avatar)
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
      storage.set(constant.roles, roles)
    },
    SET_PERMISSIONS: (state, permissions) => {
      state.permissions = permissions
      storage.set(constant.permissions, permissions)
    },
	  SET_TELEPHONE: (state, telephone) => {
      state.telephone = telephone
      storage.set(constant.telephone, telephone)
    },
		SET_ISUSER: (state, isUser) => {
		  state.isUser = isUser
		  storage.set(constant.isUser, isUser)
		},
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      const telephone = userInfo.telephone.trim()
      const password = userInfo.password
	    const method = userInfo.method
      return new Promise((resolve, reject) => {
        login(telephone, password, method).then(res => {
          setToken(`${res.data.token_type} ${res.data.access_token}`)
          commit('SET_TOKEN', `${res.data.token_type} ${res.data.access_token}`)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo({ commit }) {
      return new Promise((resolve, reject) => {
        getInfo().then(res => {
          const user = res.data
          const avatar = (user == null || user.avatar == "" || user.avatar == null) ? require("@/static/images/avatar.jpg") : user.avatar
          const name = (user == null || user.name == "" || user.name == null) ? "" : user.name
          commit('SET_ROLES', user.roles.map((item) => item.name) || ['ROLE_DEFAULT'])
          commit('SET_PERMISSIONS', user.permissions)
          commit('SET_NAME', name)
					commit('SET_TELEPHONE', user.telephone)
					commit('SET_AVATAR', avatar)
					commit('SET_CREATE_DATETIME', user.create_datetime)
					commit('SET_ISUSER', true)
					resolve(res)
				}).catch(error => {
					reject(error)
				})
			})
    },
		
		// 更新用户基本信息
		UpdateInfo({ commit }, user) {
			commit('SET_NAME', user.name)
			commit('SET_TELEPHONE', user.telephone)
		},

    // 退出系统
    LogOut({ commit }) {
      return new Promise((resolve, reject) => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        commit('SET_PERMISSIONS', [])
        removeToken()
        storage.clean()
				uni.reLaunch({ url: '/pages/login' })
        resolve()
      })
    }
  }
}

export default auth
