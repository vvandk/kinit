import config from '@/config.js'
import { getSystemBaseConfigApi } from '@/common/request/api/vadmin/system/settings.js'

const state = {
  title: '', // 标题
  logo: true, // 是否开启logo显示
  logoImage: '', // logo图片
  footer: true, // 显示页脚
  footerContent: '', // 页脚内容
  icpNumber: '', // 备案号
  version: config.appInfo.version, // 版本
  privacy: config.appInfo.privacy, // 隐私政策
  agreement: config.appInfo.agreement, // 用户协议
  siteUrl: '', // 源码地址
  WXEmail: '', // 官方邮箱
  WXPhone: '' // 服务热线
}

const mutations = {
  SET_TITLE: (state, title) => {
    state.title = title
  },
  SET_LOGO: (state, logo) => {
    state.logo = logo
  },
  SET_LOGO_IMAGE: (state, logoImage) => {
    state.logoImage = logoImage
  },
  SET_FOOTER: (state, footer) => {
    state.footer = footer
  },
  SET_FOOTER_CONTENT: (state, footerContent) => {
    state.footerContent = footerContent
  },
  SET_ICPNUMBER: (state, icpNumber) => {
    state.icpNumber = icpNumber
  },
  SET_VERSION: (state, version) => {
    state.version = version
  },
  SET_SITE_URL: (state, siteUrl) => {
    state.siteUrl = siteUrl
  },
  SET_WX_EMAIL: (state, WXEmail) => {
    state.WXEmail = WXEmail
  },
  SET_WX_PHONE: (state, WXPhone) => {
    state.WXPhone = WXPhone
  }
}

const actions = {
  // 初始化系统配置
  InitConfig({ commit }) {
    return new Promise((resolve, reject) => {
      getSystemBaseConfigApi()
        .then((res) => {
          commit('SET_TITLE', res.data.web_title || 'Kinit')
          commit('SET_LOGO_IMAGE', config.baseUrl + (res.data.web_logo || '/media/system/logo.png'))
          commit('SET_FOOTER_CONTENT', res.data.web_copyright || 'Copyright ©2022-present K')
          commit('SET_ICPNUMBER', res.data.web_icp_number || '')
          commit('SET_SITE_URL', res.data.wx_server_site || '')
          commit('SET_WX_EMAIL', res.data.wx_server_email || '')
          commit('SET_WX_PHONE', res.data.wx_server_phone || '')
          resolve()
        })
        .catch((error) => {
          reject(error)
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
