<template>
  <view class="about-container">
    <view class="header-section text-center">
      <image style="width: 150rpx; height: 150rpx" :src="logoImage" mode="widthFix"> </image>
      <uni-title type="h2" :title="title"></uni-title>
    </view>

    <view class="content-section">
      <view class="menu-list">
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>版本信息</view>
            <view class="text-right">v{{ version }}</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>官方邮箱</view>
            <view class="text-right">{{ WXEmail }}</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>服务热线</view>
            <view class="text-right">{{ WXPhone }}</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>公司网站</view>
            <view class="text-right">
              <uni-link :href="siteUrl" :text="siteUrl" show-under-line="false"></uni-link>
            </view>
          </view>
        </view>
      </view>
    </view>

    <view class="copyright">
      <view>{{ footerContent }}</view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
  },
  computed: {
    version() {
      return this.$store.state.app.version
    },
    title() {
      return this.$store.state.app.title
    },
    logoImage() {
      return this.$store.state.app.logoImage
    },
    siteUrl() {
      return this.$store.state.app.siteUrl
    },
    WXEmail() {
      return this.$store.state.app.WXEmail
    },
    WXPhone() {
      return this.$store.state.app.WXPhone
    },
    footerContent() {
      return this.$store.state.app.footerContent
    }
  }
}
</script>

<style lang="scss">
page {
  background-color: #f8f8f8;
}

.copyright {
  margin-top: 50rpx;
  text-align: center;
  line-height: 60rpx;
  color: #999;
}

.header-section {
  display: flex;
  padding: 30rpx 0 0;
  flex-direction: column;
  align-items: center;
}
</style>
