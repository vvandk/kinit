<template>
  <view v-if="params.url">
    <!-- 不支持本地路径 -->
    <web-view :webview-styles="webviewStyles" :src="`${params.url}`"></web-view>
  </view>
</template>

<script>
export default {
  props: {
    src: {
      type: [String],
      default: null
    }
  },
  data() {
    return {
      params: {},
      webviewStyles: {
        progress: {
          color: '#FF3333'
        }
      }
    }
  },
  onLoad(event) {
    this.params = event
    if (event.title) {
      uni.setNavigationBarTitle({
        title: event.title
      })
    }
  }
}
</script>
