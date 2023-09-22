<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'dict_name',
    label: '字典名称',
    colProps: {
      span: 24
    },
    component: 'Input',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'dict_type',
    label: '字典类型',
    colProps: {
      span: 24
    },
    component: 'Input',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'disabled',
    label: '是否禁用',
    colProps: {
      span: 24
    },
    component: 'RadioGroup',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '启用',
          value: false
        },
        {
          label: '禁用',
          value: true
        }
      ]
    },
    value: false,
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'remark',
    label: '备注',
    colProps: {
      span: 24
    },
    component: 'Input'
  }
])

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await getFormData()
    return formData
  }
}

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    setValues(currentRow)
  },
  {
    deep: true,
    immediate: true
  }
)

defineExpose({
  submit
})
</script>

<template>
  <Form @register="formRegister" :schema="formSchema" />
</template>
