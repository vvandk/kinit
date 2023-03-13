// 微信存储：https://developers.weixin.qq.com/miniprogram/dev/framework/ability/storage.html
// 微信登录
// 微信小程序登录流程：https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/login.html
// 登录失败的原因可能是因为没将后台IP添加到白名单

import { mapGetters } from 'vuex'
import { setUserOpenid } from '@/common/request/api/login.js'
import { toast } from '@/common/utils/common'

export const wxLoginMixins = {
  computed: {
    ...mapGetters(['isUserOpenid'])
  },
  data() {
    return {}
  },
  methods: {
    onGetPhoneNumber(e) {
      return new Promise((resolve, reject) => {
        // 获取手机号官方文档：https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html
        if (e.detail.errMsg === 'getPhoneNumber:fail user deny') {
          // 用户拒绝授权
          toast('已取消授权')
          reject('已取消授权')
        } else if (e.detail.errMsg === 'getPhoneNumber:fail no permission') {
          // 微信公众平台未认证或未使用企业认证
          toast('微信公众平台未认证或未使用企业认证')
          reject('微信公众平台未认证或未使用企业认证')
        } else if (e.detail.errMsg === 'getPhoneNumber:ok') {
          // code换取用户手机号。 每个code只能使用一次，code的有效期为5min
          this.$store.dispatch('auth/wxLogin', e.detail.code).then((res) => {
            this.setOpenid()
            this.$store.dispatch('auth/GetInfo').then((result) => {
              resolve(result)
            })
          })
        } else {
          toast('授权失败')
          reject('授权失败')
        }
      })
    },
    setOpenid() {
      let self = this
      // uniapp 官方文档：https://uniapp.dcloud.io/api/plugins/login.html#login
      if (self.isUserOpenid) {
        return
      }
      uni.login({
        provider: 'weixin',
        success: function (loginRes) {
          if (loginRes.code) {
            setUserOpenid(loginRes.code).then(() => {
              // console.log("更新openid成功", res)
              self.$store.commit('auth/SET_IS_USER_OPENID', true)
            })
          } else {
            console.log('登录失败！获取code失败！' + loginRes.errMsg)
          }
        }
      })
    }
  }
}
