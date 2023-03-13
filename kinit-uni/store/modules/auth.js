import storage from '@/common/utils/storage'
import { auth } from '@/common/utils/constant'
import { getInfo, wxCodeLogin, login } from '@/common/request/api/login'
import {
  getToken,
  setToken,
  removeToken,
  getRefreshToken,
  setRefreshToken,
  removeRefreshToken
} from '@/common/utils/auth'

const state = {
  token: getToken(),
  refreshToken: getRefreshToken(),
  isUser: storage.get(auth.isUser) || false,
  isUserOpenid: storage.get(auth.isUserOpenid) || false,
  isResetPassword: storage.get(auth.isResetPassword) || false,
  name: storage.get(auth.name),
  nickname: storage.get(auth.nickname),
  gender: storage.get(auth.gender),
  telephone: storage.get(auth.telephone),
  avatar: storage.get(auth.avatar),
  createDatetime: storage.get(auth.createDatetime),
  roles: storage.get(auth.roles),
  permissions: storage.get(auth.permissions)
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_REFRESH_TOKEN: (state, refreshToken) => {
    state.refreshToken = refreshToken
    setRefreshToken(refreshToken)
  },
  SET_IS_USER_OPENID: (state, isUserOpenid) => {
    state.isUserOpenid = isUserOpenid
    storage.set(auth.isUserOpenid, isUserOpenid)
  },
  SET_IS_RESET_PASSWORD: (state, isResetPassword) => {
    state.isResetPassword = isResetPassword
    storage.set(auth.isResetPassword, isResetPassword)
  },
  SET_NAME: (state, name) => {
    state.name = name
    storage.set(auth.name, name)
  },
  SET_GENDER: (state, gender) => {
    state.gender = gender
    storage.set(auth.gender, gender)
  },
  SET_NICKNAME: (state, nickname) => {
    state.nickname = nickname
    storage.set(auth.nickname, nickname)
  },
  SET_CREATE_DATETIME: (state, createDatetime) => {
    state.createDatetime = createDatetime
    storage.set(auth.createDatetime, createDatetime)
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
    storage.set(auth.avatar, avatar)
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
    storage.set(auth.roles, roles)
  },
  SET_PERMISSIONS: (state, permissions) => {
    state.permissions = permissions
    storage.set(auth.permissions, permissions)
  },
  SET_TELEPHONE: (state, telephone) => {
    state.telephone = telephone
    storage.set(auth.telephone, telephone)
  },
  SET_ISUSER: (state, isUser) => {
    state.isUser = isUser
    storage.set(auth.isUser, isUser)
  }
}

const actions = {
  // 手机号密码登录
  Login({ commit }, userInfo) {
    const telephone = userInfo.telephone.trim()
    const password = userInfo.password
    return new Promise((resolve, reject) => {
      login(telephone, password)
        .then((res) => {
          setToken(`${res.data.token_type} ${res.data.access_token}`)
          commit('SET_TOKEN', `${res.data.token_type} ${res.data.access_token}`)
          commit('SET_REFRESH_TOKEN', res.data.refresh_token)
          commit('SET_IS_USER_OPENID', res.data.is_wx_server_openid)
          commit('SET_IS_RESET_PASSWORD', res.data.is_reset_password)
          resolve(res)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },

  // 微信一键登录
  // 微信文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html
  wxLogin({ commit }, code) {
    return new Promise((resolve, reject) => {
      wxCodeLogin(code)
        .then((res) => {
          setToken(`${res.data.token_type} ${res.data.access_token}`)
          commit('SET_TOKEN', `${res.data.token_type} ${res.data.access_token}`)
          commit('SET_REFRESH_TOKEN', res.data.refresh_token)
          commit('SET_IS_USER_OPENID', res.data.is_wx_server_openid)
          commit('SET_IS_RESET_PASSWORD', res.data.is_reset_password)
          resolve(res)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },

  // 获取用户信息
  GetInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getInfo()
        .then((res) => {
          const user = res.data
          const avatar =
            user == null || user.avatar == '' || user.avatar == null
              ? 'https://vv-reserve.oss-cn-hangzhou.aliyuncs.com/avatar/2023-01-27/1674820804e81e7631.png'
              : user.avatar
          const name = user == null || user.name == '' || user.name == null ? '' : user.name
          commit('SET_ROLES', user.roles.map((item) => item.name) || ['ROLE_DEFAULT'])
          commit('SET_PERMISSIONS', user.permissions)
          commit('SET_NAME', name)
          commit('SET_NICKNAME', user.nickname)
          commit('SET_GENDER', user.gender)
          commit('SET_TELEPHONE', user.telephone)
          commit('SET_AVATAR', avatar)
          commit('SET_CREATE_DATETIME', user.create_datetime)
          commit('SET_ISUSER', true)
          resolve(res)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },

  // 更新用户基本信息
  UpdateInfo({ commit }, user) {
    commit('SET_NAME', user.name)
    commit('SET_NICKNAME', user.nickname)
    commit('SET_GENDER', user.gender)
    commit('SET_TELEPHONE', user.telephone)
  },

  // 退出系统
  LogOut({ commit }) {
    return new Promise((resolve, reject) => {
      commit('SET_TOKEN', '')
      commit('SET_REFRESH_TOKEN', '')
      commit('SET_ROLES', [])
      commit('SET_PERMISSIONS', [])
      commit('SET_NAME', '')
      commit('SET_NICKNAME', '')
      commit('SET_GENDER', '')
      commit('SET_TELEPHONE', '')
      commit('SET_AVATAR', '')
      commit('SET_CREATE_DATETIME', '')
      commit('SET_IS_USER_OPENID', false)
      commit('SET_IS_RESET_PASSWORD', false)
      commit('SET_ISUSER', false)
      removeToken()
      removeRefreshToken()
      storage.clean()
      uni.reLaunch({
        url: '/pages/login/login',
        complete: () => {
          resolve()
        }
      })
    })
  }
}

export default {
  namespaced: true, // 使用命名空间去访问模块中属性，user/login
  state,
  mutations,
  actions
}
