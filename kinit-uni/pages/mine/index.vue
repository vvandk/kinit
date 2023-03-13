<template>
  <view class="mine-container" :style="{ height: `${windowHeight}px` }">
    <!--顶部个人信息栏-->
    <view class="header-section">
      <view class="flex padding justify-between">
        <view class="flex align-center">
          <view v-if="!avatar" class="cu-avatar xl round bg-white">
            <view class="iconfont icon-people text-gray icon"></view>
          </view>
          <image
            v-if="avatar"
            :src="avatar"
            class="cu-avatar xl round"
            mode="aspectFill"
            @click="handleToAvatar"
          >
          </image>
          <view v-if="!name" class="login-tip" @click="handleToLogin"> 点击登录 </view>
          <view v-if="name" class="user-info" @click="handleToInfo">
            <view class="u_title">
              {{ name }}
            </view>
          </view>
        </view>
        <view class="flex align-center" @click="handleToInfo">
          <text style="font-size: 30rpx">个人信息</text>
          <view class="iconfont icon-right1"></view>
        </view>
      </view>
    </view>

    <view class="content-section">
      <view class="mine-actions grid col-4 text-center">
        <view class="action-item" @click="handleJiaoLiuQun">
          <view class="iconfont icon-xitongjiaose text-pink icon"></view>
          <text class="text">交流群</text>
        </view>
        <view class="action-item" @click="handleBuilding">
          <view class="iconfont icon-kefu text-blue icon"></view>
          <text class="text">在线客服</text>
        </view>
        <view class="action-item" @click="handleBuilding">
          <view class="iconfont icon-yaoqingdaoshi text-mauve icon"></view>
          <text class="text">意见反馈</text>
        </view>
        <view class="action-item" @click="praiseMe">
          <view class="iconfont icon-dianzan text-green icon"></view>
          <view style="height: 0px" :animation="animationData" class="praise-me animation-opacity">
            +1
          </view>
          <text class="text">点赞我们</text>
        </view>
      </view>

      <view class="menu-list">
        <view class="list-cell list-cell-arrow" @click="handleToEditInfo">
          <view class="menu-item-box">
            <view class="iconfont icon-user menu-icon"></view>
            <view>编辑资料</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow" @click="handleHelp">
          <view class="menu-item-box">
            <view class="iconfont icon-wenti1-copy menu-icon"></view>
            <view>常见问题</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow" @click="handleAbout">
          <view class="menu-item-box">
            <view class="iconfont icon-aixin menu-icon"></view>
            <view>关于我们</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow" @click="handleToSetting">
          <view class="menu-item-box">
            <view class="iconfont icon-shezhi2 menu-icon"></view>
            <view>应用设置</view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      animation: '',
      animationData: {}
    }
  },
  onLoad() {
    // 1 在页面创建的时候，创建一个临时动画对象
    this.animation = uni.createAnimation()
    this.animationData = {}
  },
  onUnload() {
    // 5 页面卸载的时候，清除动画数据
    this.animationData = {}
  },
  computed: {
    version() {
      return this.$store.state.app.version
    },
    name() {
      return this.$store.state.auth.name
    },
    avatar() {
      return this.$store.state.auth.avatar
    },
    windowHeight() {
      return uni.getSystemInfoSync().windowHeight - 50
    }
  },
  methods: {
    handleToInfo() {
      this.$tab.navigateTo('/pages/mine/info/index')
    },
    handleToEditInfo() {
      this.$tab.navigateTo('/pages/mine/info/edit')
    },
    handleToSetting() {
      this.$tab.navigateTo('/pages/mine/setting/index')
    },
    handleToLogin() {
      this.$tab.reLaunch('/pages/login/login')
    },
    handleToAvatar() {
      this.$tab.navigateTo('/pages/mine/avatar/index')
    },
    handleLogout() {
      this.$modal.confirm('确定注销并退出系统吗？').then(() => {
        this.$store.dispatch('LogOut').then(() => {
          this.$tab.reLaunch('/pages/index')
        })
      })
    },
    handleHelp() {
      this.$tab.navigateTo('/pages/mine/help/issue/index')
    },
    handleAbout() {
      this.$tab.navigateTo('/pages/mine/about/index')
    },
    handleJiaoLiuQun() {
      this.$modal.showToast('模块建设中~')
    },
    handleBuilding() {
      this.$modal.showToast('模块建设中~')
    },
    // 实现点赞动画效果
    praiseMe() {
      // 2 调用 step() 来表示一组动画完成
      this.animation.translateY(-90).opacity(1).step({
        duration: 400
      })

      // 3 通过动画实例的export方法导出动画数据传递给组件的animation属性
      this.animationData = this.animation.export()

      // 4 还原动画
      setTimeout(() => {
        this.animation.translateY(0).opacity(0).step({
          duration: 0
        })
        this.animationData = this.animation.export()
      }, 300)
    }
  }
}
</script>

<style lang="scss" scoped>
.praise-me {
  font-size: 14px;
  color: #feab2a;
}

.animation-opacity {
  font-weight: bold;
  opacity: 0;
}

page {
  background-color: #f5f6f7;
}

.mine-container {
  width: 100%;
  height: 100%;

  .header-section {
    padding: 15px 15px 45px 15px;
    background-color: #3c96f3;
    color: white;

    .login-tip {
      font-size: 18px;
      margin-left: 10px;
    }

    .cu-avatar {
      border: 2px solid #eaeaea;

      .icon {
        font-size: 40px;
      }
    }

    .user-info {
      margin-left: 15px;

      .u_title {
        font-size: 37rpx;
        line-height: 30px;
      }
    }
  }

  .content-section {
    position: relative;
    top: -50px;

    .mine-actions {
      margin: 15px 15px;
      padding: 20px 0px;
      border-radius: 8px;
      background-color: white;

      .action-item {
        .icon {
          font-size: 28px;
        }

        .text {
          display: block;
          font-size: 13px;
          margin: 8px 0px;
        }
      }
    }
  }
}
</style>
