<script setup lang="ts">
import { ElCarousel, ElCarouselItem, ElImage, ElCard } from 'element-plus'
import Charts from './components/Charts.vue'
import { getBannersApi } from '@/api/dashboard/analysis'
import { ref } from 'vue'
import { AnalysisBannersTypes } from '@/api/dashboard/analysis/types'

const banners = ref([] as AnalysisBannersTypes[])
const loading = ref(false)

const getBanners = async () => {
  loading.value = true
  const res = await getBannersApi()
  if (res) {
    banners.value = res.data
  }
  loading.value = false
}

getBanners()
</script>

<template>
  <div class="mb-20px" style="display: flex; justify-content: center; min-width: 1680px">
    <ElCard shadow="never" class="w-1680px">
      <!-- 添加 v-if 解决显示动态数据时，默认会显示一个空白元素 -->
      <ElCarousel v-loading="loading" v-if="banners.length > 0" height="500px" :interval="5000">
        <ElCarouselItem v-for="item in banners" :key="item.id">
          <ElImage :src="item.image" />
        </ElCarouselItem>
      </ElCarousel>
    </ElCard>
  </div>
  <Charts />
</template>

<style scoped>
.el-carousel__item h3 {
  display: flex;
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
