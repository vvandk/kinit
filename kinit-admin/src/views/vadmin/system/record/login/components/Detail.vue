<script setup lang="ts">
import { PropType, ref } from 'vue'
import { Descriptions } from '@/components/Descriptions'
import { ElSwitch } from 'element-plus'
// json内容展示组件
import { JsonViewer } from 'vue3-json-viewer'
import 'vue3-json-viewer/dist/index.css'
import { DescriptionsSchema } from '@/types/descriptions'
import { DictDetail, selectDictLabel } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'

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

const platformOptions = ref<DictDetail[]>([])
const loginMethodOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_platform', 'sys_vadmin_login_method'])
  platformOptions.value = dictOptions.sys_vadmin_platform
  loginMethodOptions.value = dictOptions.sys_vadmin_login_method
}

getOptions()
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

    <template #platform="{ row }">
      {{ selectDictLabel(platformOptions, row.platform) }}
    </template>

    <template #login_method="{ row }">
      {{ selectDictLabel(loginMethodOptions, row.login_method) }}
    </template>
  </Descriptions>
</template>
