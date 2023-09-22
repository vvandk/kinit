<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { getDictTypeOptionsApi } from '@/api/vadmin/system/dict'
import { propTypes } from '@/utils/propTypes'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  },
  dictTypeId: propTypes.number.def(undefined)
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'dict_type_id',
    label: '字典类型',
    colProps: {
      span: 24
    },
    component: 'Select',
    componentProps: {
      clearable: false,
      style: {
        width: '100%'
      }
    },
    optionApi: async () => {
      const res = await getDictTypeOptionsApi()
      return res.data
    },
    formItemProps: {
      rules: [required()]
    },
    value: props.dictTypeId
  },
  {
    field: 'label',
    label: '字典标签',
    colProps: {
      span: 24
    },
    component: 'Input',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'value',
    label: '字典键值',
    colProps: {
      span: 24
    },
    component: 'Input',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'order',
    label: '排序',
    colProps: {
      span: 24
    },
    component: 'InputNumber',
    componentProps: {
      style: {
        width: '50%'
      }
    },
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'is_default',
    label: '是否默认',
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
          label: '是',
          value: true
        },
        {
          label: '否',
          value: false
        }
      ]
    },
    value: false,
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
