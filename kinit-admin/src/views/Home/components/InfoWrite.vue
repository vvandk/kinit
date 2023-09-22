<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { reactive, ref } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { ElButton, ElMessage } from 'element-plus'
import { postCurrentUserUpdateInfo } from '@/api/vadmin/auth/user'

const { required, isTelephone } = useValidator()

const authStore = useAuthStoreWithOut()

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '用户名称',
    component: 'Input',
    colProps: {
      span: 24
    },
    formItemProps: {
      rules: [required()]
    },
    componentProps: {
      style: {
        width: '50%'
      }
    }
  },
  {
    field: 'nickname',
    label: '用户昵称',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '50%'
      }
    }
  },
  {
    field: 'telephone',
    label: '手机号',
    component: 'Input',
    colProps: {
      span: 24
    },
    formItemProps: {
      rules: [required(), { validator: isTelephone, trigger: 'blur' }]
    },
    componentProps: {
      style: {
        width: '50%'
      },
      maxlength: 11
    }
  },
  {
    field: 'gender',
    label: '性别',
    colProps: {
      span: 24
    },
    formItemProps: {
      rules: [required()]
    },
    component: 'RadioGroup',
    componentProps: {
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
    }
  },
  {
    field: 'save',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="w-[50%]">
                <ElButton loading={loading.value} type="primary" class="w-[100%]" onClick={save}>
                  保存
                </ElButton>
              </div>
            </>
          )
        }
      }
    }
  }
])

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

setValues(authStore.getUser)
const loading = ref(false)

// 提交
const save = async () => {
  if (authStore.getUser.id === 1) {
    return ElMessage.warning('编辑账号为演示账号，无权限操作！')
  }
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    loading.value = true
    const formData = await getFormData()
    try {
      const res = await postCurrentUserUpdateInfo(formData)
      if (res) {
        authStore.updateUser(res.data)
        ElMessage.success('保存成功')
      }
    } finally {
      loading.value = false
    }
  }
}
</script>

<template>
  <Form
    @register="formRegister"
    :schema="formSchema"
    hide-required-asterisk
    class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
  />
</template>
