<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { schema } from './components/email.data'
import { ElButton } from 'element-plus'
import { getSystemSettingsApi, putSystemSettingsApi } from '@/api/vadmin/system/settings'
import { ref, unref } from 'vue'
import { ElMessage } from 'element-plus'
import { propTypes } from '@/utils/propTypes'

const props = defineProps({
  tabId: propTypes.number
})

const { register, methods, elFormRef } = useForm({
  schema: schema
})

const { setValues } = methods

let formData = ref({} as Recordable)

const getData = async () => {
  const res = await getSystemSettingsApi({ tab_id: props.tabId })
  if (res) {
    setValues(res.data)
    formData.value = res.data
  }
}

const loading = ref(false)

const save = async () => {
  const formRef = unref(elFormRef)
  await formRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      let data = await methods.getFormData()
      if (!data) {
        loading.value = false
        return ElMessage.error('未获取到数据')
      }
      try {
        const res = await putSystemSettingsApi(data)
        if (res) {
          getData()
          return ElMessage.success('更新成功')
        }
      } finally {
        loading.value = false
      }
    }
  })
}

getData()
</script>

<template>
  <Form @register="register">
    <template #active>
      <ElButton :loading="loading" type="primary" @click="save">立即提交</ElButton>
    </template>
  </Form>
</template>

<style scoped lang="less"></style>
