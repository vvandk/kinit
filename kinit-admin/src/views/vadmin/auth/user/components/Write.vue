<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { getRoleOptionsApi } from '@/api/vadmin/auth/role'

const { required, isTelephone, isEmail } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '用户名称',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'nickname',
    label: '用户昵称',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'telephone',
    label: '手机号码',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'email',
    label: '邮箱',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'gender',
    label: '性别',
    colProps: {
      span: 12
    },
    component: 'RadioGroup',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '男',
          value: '0'
        },
        {
          label: '女',
          value: '1'
        }
      ]
    },
    value: '0'
  },
  {
    field: '',
    label: '默认密码',
    colProps: {
      span: 12
    },
    component: 'Text',
    componentProps: {
      style: {
        width: '100%'
      }
    },
    value: '手机号后六位',
    ifshow: (values) => values.id === undefined
  },
  {
    field: 'is_staff',
    label: '工作人员',
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
    value: true
  },
  {
    field: 'is_active',
    label: '状态',
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
          label: '正常',
          value: true
        },
        {
          label: '停用',
          value: false
        }
      ]
    },
    value: true
  },
  {
    field: 'role_ids',
    label: '角色',
    colProps: {
      span: 24
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: true
    },
    optionApi: async () => {
      const res = await getRoleOptionsApi()
      return res.data
    },
    value: [],
    ifshow: (values) => values.is_staff
  }
])

const rules = reactive({
  name: [required()],
  is_active: [required()],
  is_staff: [required()],
  role_ids: [required()],
  telephone: [required(), { validator: isTelephone, trigger: 'blur' }],
  email: [{ validator: isEmail, trigger: 'blur' }]
})

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
  <Form :rules="rules" @register="formRegister" :schema="formSchema" />
</template>
