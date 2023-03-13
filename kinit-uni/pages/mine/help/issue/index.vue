<template>
  <view class="help-container">
    <view v-for="(item, findex) in list" :key="findex" :title="item.name" class="list-title">
      <view class="text-title">
        <view>{{ item.name }}</view>
      </view>
      <view class="childList">
        <view
          v-for="(issue, zindex) in item.issues"
          :key="zindex"
          class="question"
          hover-class="hover"
          @click="handleText(issue)"
        >
          <view class="text-item">{{ issue.title }}</view>
          <view v-if="zindex !== item.issues.length - 1" class="line"></view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getIssueCategoryList } from '@/common/request/api/vadmin/help/issue.js'

export default {
  data() {
    return {
      list: []
    }
  },
  onLoad() {
    getIssueCategoryList().then((res) => {
      this.list = res.data
    })
  },
  methods: {
    handleText(item) {
      this.$tab.navigateTo(`/pages/mine/help/issue/info?id=${item.id}`)
    }
  }
}
</script>

<style lang="scss">
page {
  background-color: #f8f8f8;
}

.help-container {
  margin-bottom: 100rpx;
  padding: 30rpx;
}

.list-title {
  margin-bottom: 30rpx;
}

.childList {
  background: #ffffff;
  box-shadow: 0px 0px 10rpx rgba(193, 193, 193, 0.2);
  border-radius: 16rpx;
  margin-top: 10rpx;
}

.line {
  width: 100%;
  height: 1rpx;
  background-color: #f5f5f5;
}

.text-title {
  color: #303133;
  font-size: 32rpx;
  font-weight: bold;
  margin-left: 10rpx;
}

.text-item {
  font-size: 28rpx;
  padding: 24rpx;
}

.question {
  color: #606266;
  font-size: 28rpx;
}
</style>
