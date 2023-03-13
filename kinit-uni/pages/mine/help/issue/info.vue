<template>
  <view>
    <uni-card v-if="isSuccess" class="view-title">
      <u--text :text="model.title" bold></u--text>
      <rich-text class="uni-body view-content" :nodes="model.content"></rich-text>
    </uni-card>
    <u-empty
      v-else
      mode="data"
      icon="https://cdn.uviewui.com/uview/empty/data.png"
      :margin-top="100"
      :width="300"
      :height="300"
    >
    </u-empty>
  </view>
</template>

<script>
import { getIssue, updateIssueAddViewNumber } from '@/common/request/api/vadmin/help/issue.js'

export default {
  data() {
    return {
      isSuccess: true,
      model: {},
      dataId: null
    }
  },
  onLoad(options) {
    if (options.query) {
      this.dataId = options.query.id
    } else if (options) {
      this.dataId = options.id
    }
    this.getData()
  },
  methods: {
    getData() {
      if (!this.dataId) {
        return
      }
      getIssue(this.dataId)
        .then((res) => {
          this.model = res.data
          uni.setNavigationBarTitle({
            title: res.data.title
          })
          updateIssueAddViewNumber(this.dataId)
        })
        .catch(() => {
          this.isSuccess = false
        })
    }
  }
}
</script>

<style scoped>
page {
  background-color: #ffffff;
}

.view-content {
  font-size: 26rpx;
  padding: 12px 5px 0;
  color: #333;
  line-height: 24px;
  font-weight: normal;
}
</style>
