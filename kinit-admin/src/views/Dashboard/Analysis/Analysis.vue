<script setup lang="ts">
import { ref } from 'vue'
import Finance from './components/Finance.vue'
import { ElTabs, ElTabPane } from 'element-plus'
import User from './components/User.vue'
import { ContentWrap } from '@/components/ContentWrap'

defineOptions({
  name: 'DashboardAnalysis'
})

const activeName = ref('user')
</script>

<template>
  <ContentWrap>
    <ElTabs v-model="activeName">
      <ElTabPane label="财务分析" name="finance" :lazy="true">
        <Finance />
      </ElTabPane>
      <ElTabPane label="客户分析" name="user" :lazy="true">
        <User />
      </ElTabPane>
    </ElTabs>
  </ContentWrap>
</template>

<style scoped></style>
