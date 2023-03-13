<template>
  <view class="normal-login-container">
    <view class="logo-content align-center justify-center flex">
      <image v-if="logo" style="width: 100rpx; height: 100rpx" :src="logoImage" mode="widthFix">
      </image>
      <text class="title">{{ title }}</text>
    </view>
    <view class="login-form-content">
      <view class="input-item flex align-center">
        <view class="iconfont icon-user icon"></view>
        <input
          v-model="loginForm.telephone"
          class="input"
          type="text"
          placeholder="请输入手机号"
          maxlength="30"
        />
      </view>
      <view class="input-item flex align-center">
        <view class="iconfont icon-password icon"></view>
        <input
          v-model="loginForm.password"
          type="password"
          class="input"
          placeholder="请输入密码"
          maxlength="20"
        />
      </view>
      <view class="action-btn">
        <!-- <button @click="handleLogin" class="login-btn cu-btn block bg-blue lg round">登录</button> -->
        <u-button type="primary" text="登录" shape="circle" @click="handleLogin"></u-button>
      </view>
    </view>

    <view class="xieyi text-center">
      <text class="text-grey1">登录即代表同意</text>
      <text class="text-blue" @click="handleUserAgrement">《用户协议》</text>
      <text class="text-blue" @click="handlePrivacy">《隐私协议》</text>
    </view>

    <view class="footer text-center">
      <u-button
        type="primary"
        text="微信一键登录"
        shape="circle"
        open-type="getPhoneNumber"
        @getphonenumber="wxLogin"
      ></u-button>
    </view>
  </view>
</template>

<script>
import { wxLoginMixins } from '@/common/mixins/auth.js'

export default {
  mixins: [wxLoginMixins],
  data() {
    return {
      loginForm: {
        telephone: '15020221010',
        password: 'kinit2022'
      }
    }
  },
  computed: {
    title() {
      return this.$store.state.app.title
    },
    logo() {
      return this.$store.state.app.logo
    },
    logoImage() {
      return this.$store.state.app.logoImage
    },
    privacy() {
      return this.$store.state.app.privacy
    },
    agreement() {
      return this.$store.state.app.agreement
    },
    isResetPassword() {
      return this.$store.state.auth.isResetPassword
    }
  },
  methods: {
    // 隐私政策
    handlePrivacy() {
      const title = '隐私政策'
      this.$tab.navigateTo(`/pages/common/webview/index?title=${title}&url=${this.privacy}`)
    },
    // 用户协议
    handleUserAgrement() {
      const title = '用户协议'
      this.$tab.navigateTo(`/pages/common/webview/index?title=${title}&url=${this.agreement}`)
    },
    // 登录方法
    async handleLogin() {
      if (this.loginForm.telephone === '') {
        this.$modal.msgError('请输入您的手机号')
      } else if (this.loginForm.password === '') {
        this.$modal.msgError('请输入您的密码')
      } else {
        this.$modal.loading('正在登录中...')
        this.pwdLogin()
      }
    },
    // 密码登录
    async pwdLogin() {
      this.$store.dispatch('auth/Login', this.loginForm).then(() => {
        this.$modal.closeLoading()
        this.loginSuccess()
      })
    },
    // 登录成功后，处理函数
    loginSuccess() {
      if (this.isResetPassword) {
        this.$tab.reLaunch('/pages/index')
      } else {
        this.$tab.reLaunch('/pages/mine/pwd/index')
      }
    },
    // 微信一键登录
    wxLogin(detail) {
      this.onGetPhoneNumber(detail).then((res) => {
        this.loginSuccess()
      })
    }
  }
}
</script>

<style lang="scss">
page {
  background-color: #ffffff;
}

.normal-login-container {
  width: 100%;
  height: 100vh;
  position: relative;

  .logo-content {
    width: 100%;
    font-size: 21px;
    text-align: center;
    padding-top: 15%;

    image {
      border-radius: 4px;
    }

    .title {
      margin-left: 10px;
    }
  }

  .login-form-content {
    text-align: center;
    margin: 20px auto;
    margin-top: 15%;
    width: 80%;

    .input-item {
      margin: 20px auto;
      background-color: #f5f6f7;
      height: 45px;
      border-radius: 20px;

      .icon {
        font-size: 38rpx;
        margin-left: 10px;
        color: #999;
      }

      .input {
        width: 100%;
        font-size: 14px;
        line-height: 20px;
        text-align: left;
        padding-left: 15px;
      }
    }

    .login-btn {
      margin-top: 40px;
      height: 45px;
    }

    .xieyi {
      color: #333;
      margin-top: 20px;
    }
  }

  .easyinput {
    width: 100%;
  }

  .footer {
    margin: 20px auto;
    width: 80%;
    position: absolute;
    bottom: 30px;
    left: 10%;
  }
}

.login-code-img {
  height: 45px;
}
</style>
