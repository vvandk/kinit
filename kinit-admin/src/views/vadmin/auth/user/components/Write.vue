<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { schema } from './user.data'
import { getRoleOptionsApi } from '@/api/vadmin/auth/role'

const { required, isEmail, isTelephone } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  }
})

const rules = reactive({
  name: [required()],
  is_active: [required()],
  is_staff: [required()],
  role_ids: [required()],
  telephone: [required(), { validator: isTelephone, trigger: 'blur' }],
  email: [required(), { validator: isEmail, trigger: 'blur' }]
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

const getRoleOptions = async () => {
  const res = await getRoleOptionsApi()
  if (res) {
    const { setSchema } = methods
    setSchema([
      {
        field: 'role_ids',
        path: 'componentProps.options',
        value: res.data
      }
    ])
  }
}

getRoleOptions()

defineExpose({
  elFormRef,
  getFormData: methods.getFormData
})
</script>

<template>
  <Form :rules="rules" @register="register" />
</template>
