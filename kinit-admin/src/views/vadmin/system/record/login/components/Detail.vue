<script setup lang="ts">
import { PropType } from 'vue'
import { Descriptions } from '@/components/Descriptions'
import { ElSwitch } from 'element-plus'
// json内容展示组件
import { JsonViewer } from 'vue3-json-viewer'
import 'vue3-json-viewer/dist/index.css'
import { DescriptionsSchema } from '@/types/descriptions'

defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  },
  detailSchema: {
    type: Array as PropType<DescriptionsSchema[]>,
    default: () => []
  }
})
</script>

<template>
  <Descriptions :schema="detailSchema" :data="currentRow || {}">
    <template #status="{ row }">
      <ElSwitch :value="row.status" size="small" disabled />
    </template>

    <template #response="{ row }">
      <JsonViewer :value="JSON.parse(row.response)" copyable boxed sort />
    </template>

    <template #request="{ row }">
      <JsonViewer :value="JSON.parse(row.request)" copyable boxed sort />
    </template>
  </Descriptions>
</template>
