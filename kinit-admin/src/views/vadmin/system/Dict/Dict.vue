<script setup lang="ts">
import { ElRow, ElCol } from 'element-plus'
import DictDetail from './Detail/DictDetail.vue'
import DcitType from './Type/DictType.vue'
import { ref } from 'vue'

defineOptions({
  name: 'SystemDict'
})

const dictTypeId = ref<number | undefined>()

const updateDictTypeId = (value: number | undefined) => {
  dictTypeId.value = value
}
</script>

<template>
  <ElRow>
    <ElCol :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
      <DcitType @update-dict-type-id="updateDictTypeId" />
    </ElCol>
    <ElCol :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
      <DictDetail :dict-type-id="dictTypeId" />
    </ElCol>
  </ElRow>
</template>

<style scoped lang="less"></style>
