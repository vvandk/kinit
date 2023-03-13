<template>
  <view class="work-container">
    <!-- 轮播图 -->
    <u-swiper
      :list="images"
      indicator
      indicator-mode="line"
      circular
      :height="`${windowWidth / 2.5}px`"
    ></u-swiper>

    <!-- 宫格组件 -->
    <view class="grid-body">
      <u-grid :border="false" col="3" @click="changeGrid">
        <u-grid-item v-for="(item, index) in baseList" :key="index">
          <view class="grid-item">
            <view :class="'iconfont ' + item.icon + ' grid-icon'"></view>
            <u--text :text="item.title" align="center" line-height="32px"></u--text>
          </view>
        </u-grid-item>
      </u-grid>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      windowWidth: uni.getSystemInfoSync().windowWidth,
      images: [
        'https://ktianc.oss-cn-beijing.aliyuncs.com/kinit/system/banner/2022-11-14/1.jpg',
        '/static/images/banner/banner03.jpg',
        '/static/images/banner/banner03.jpg'
      ],
      baseList: [
        {
          icon: 'icon-user1',
          title: '用户管理'
        },
        {
          icon: 'icon-users',
          title: '角色管理'
        },
        {
          icon: 'icon-caidan3',
          title: '菜单管理'
        },
        {
          icon: 'icon-shezhitianchong',
          title: '系统配置'
        },
        {
          icon: 'icon-changguizidian',
          title: '字典管理'
        },
        {
          icon: 'icon-rizhi',
          title: '日志管理'
        }
      ]
    }
  },
  methods: {
    changeGrid(e) {
      this.$modal.showToast('模块建设中~')
    }
  }
}
</script>

<style lang="scss">
page {
  background-color: #fff;
  min-height: 100%;
  height: auto;
}
</style>

<style lang="scss" scoped>
.grid-body {
  margin-top: 60rpx;

  .grid-item {
    margin-bottom: 30rpx;
    text-align: center;
  }

  .grid-icon {
    font-size: 40rpx;
  }
}
</style>
