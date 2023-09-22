<script setup lang="ts">
import { ref } from 'vue'
import Finance from './components/Finance.vue'
import { ElTabs, ElTabPane } from 'element-plus'
import User from './components/User.vue'

defineOptions({
  name: 'DashboardAnalysis'
})

const activeName = ref('user')
</script>

<template>
  <div class="p-5">
    <ElTabs v-model="activeName">
      <ElTabPane label="财务分析" name="finance" :lazy="true">
        <Finance />
      </ElTabPane>
      <ElTabPane label="客户分析" name="user" :lazy="true">
        <User />
      </ElTabPane>
    </ElTabs>
  </div>
</template>

<style scoped></style>
