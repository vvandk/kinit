<template>
  <view class="content">
    <image v-if="logo" class="logo" :src="logoImage"></image>
    <view class="text-area">
      <text class="title">Hello {{ name }}</text>
    </view>
  </view>
</template>

<script>
import { wxShareMixins } from '@/common/mixins/share.js'

export default {
  mixins: [wxShareMixins],
  computed: {
    name() {
      return this.$store.state.auth.name
    },
    logo() {
      return this.$store.state.app.logo
    },
    logoImage() {
      return this.$store.state.app.logoImage
    }
  }
}
</script>

<style lang="scss">
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  .logo {
    height: 200rpx;
    width: 200rpx;
    margin-top: 200rpx;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 50rpx;
  }

  .text-area {
    display: flex;
    justify-content: center;

    .title {
      font-size: 36rpx;
      color: #8f8f94;
    }
  }
}
</style>
