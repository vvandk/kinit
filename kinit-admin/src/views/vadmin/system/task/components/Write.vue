<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { schema } from './task.data'
import { DictDetail } from '@/utils/dict'
import { ElRadioGroup, ElRadio } from 'element-plus'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  },
  execStrategyOptions: {
    type: Object as PropType<DictDetail[]>,
    default: () => null
  },
  taskGroupOptions: {
    type: Object as PropType<DictDetail[]>,
    default: () => null
  }
})

const rules = reactive({
  name: [required()],
  exec_strategy: [required()],
  expression: [{ required: true, message: '请填写表达式', trigger: 'blur' }],
  job_class: [required()]
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
  () => props.execStrategyOptions,
  (execStrategyOptions) => {
    if (!execStrategyOptions) return
    const { setSchema } = methods
    setSchema([
      {
        field: 'exec_strategy',
        path: 'componentProps.options',
        value: execStrategyOptions
      }
    ])
  },
  {
    deep: true,
    immediate: true
  }
)

watch(
  () => props.taskGroupOptions,
  (taskGroupOptions) => {
    if (!taskGroupOptions) return
    const { setSchema } = methods
    setSchema([
      {
        field: 'group',
        path: 'componentProps.options',
        value: taskGroupOptions
      }
    ])
  },
  {
    deep: true,
    immediate: true
  }
)

const handleChange = (form) => {
  form['start_date'] = null
  form['end_date'] = null
  form['expression'] = null
  elFormRef.value?.clearValidate('expression')
}

defineExpose({
  elFormRef,
  getFormData: methods.getFormData
})
</script>

<template>
  <Form :rules="rules" @register="register">
    <template #exec_strategy="form">
      <ElRadioGroup v-model="form['exec_strategy']" @change="handleChange(form)">
        <ElRadio v-for="(item, $index) in execStrategyOptions" :key="$index" :label="item.value">{{
          item.label
        }}</ElRadio>
      </ElRadioGroup>
    </template>
  </Form>
</template>
