<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { schema } from './issueCategory.data'
import { DictDetail } from '@/utils/dict'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  },
  platformOptions: {
    type: Object as PropType<DictDetail[]>,
    default: () => null
  }
})

const rules = reactive({
  name: [required()],
  platform: [required()],
  is_active: [required()]
})

const { register, methods, elFormRef } = useForm({
  schema: schema
})

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    const { setValues } = methods
    setValues(currentRow)
  },
  {
    deep: true,
    immediate: true
  }
)

watch(
  () => props.platformOptions,
  (platformOptions) => {
    if (!platformOptions) return
    const { setSchema } = methods
    setSchema([
      {
        field: 'platform',
        path: 'componentProps.options',
        value: platformOptions
      }
    ])
  },
  {
    deep: true,
    immediate: true
  }
)

defineExpose({
  elFormRef,
  getFormData: methods.getFormData
})
</script>

<template>
  <Form :rules="rules" @register="register" />
</template>
