<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { ElButton } from 'element-plus'
import { getSystemSettingsApi, putSystemSettingsApi } from '@/api/vadmin/system/settings'
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { propTypes } from '@/utils/propTypes'
import { useValidator } from '@/hooks/web/useValidator'

const { required } = useValidator()

const props = defineProps({
  tabId: propTypes.number
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'sms_access_key',
    label: 'AccessKey',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'sms_access_key_secret',
    label: 'AccessKeySecret',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'sms_sign_name_1',
    label: '短信验证码签名',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'sms_template_code_1',
    label: '短信验证码模板',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'sms_sign_name_2',
    label: '重置密码签名',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'sms_template_code_2',
    label: '重置密码模板',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'sms_send_interval',
    label: '发送频率',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'sms_valid_time',
    label: '有效时间',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'active',
    label: '',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <ElButton loading={loading.value} type="primary" onClick={save}>
                立即提交
              </ElButton>
            </>
          )
        }
      }
    }
  }
])

const rules = reactive({
  sms_access_key: [required()],
  sms_access_key_secret: [required()],
  sms_send_interval: [required()],
  sms_valid_time: [required()]
})

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

let formData = ref({} as Recordable)

const getData = async () => {
  const res = await getSystemSettingsApi({ tab_id: props.tabId })
  if (res) {
    await setValues(res.data)
    formData.value = res.data
    const elForm = await getElFormExpose()
    elForm?.clearValidate()
  }
}

const loading = ref(false)

const save = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await getFormData()
    loading.value = true
    if (!formData) {
      loading.value = false
      return ElMessage.error('未获取到数据')
    }
    try {
      const res = await putSystemSettingsApi(formData)
      if (res) {
        getData()
        return ElMessage.success('更新成功')
      }
    } finally {
      loading.value = false
    }
  }
}

getData()
</script>

<template>
  <Form :rules="rules" @register="formRegister" :schema="formSchema" />
</template>

<style lang="less"></style>
