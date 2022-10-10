<script setup lang="ts">
import { reactive, unref, ref } from 'vue'
import { Form } from '@/components/Form'
import { ElButton } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
import { postCurrentUserResetPassword } from '@/api/vadmin/auth/user'
import { useValidator } from '@/hooks/web/useValidator'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { ElMessage } from 'element-plus'

const { required } = useValidator()

const authStore = useAuthStoreWithOut()

const rules = {
  password: [
    required(),
    { min: 8, max: 16, message: '长度需为8-16个字符,请重新输入。', trigger: 'blur' }
  ],
  password_two: [
    required(),
    { min: 8, max: 16, message: '长度需为8-16个字符,请重新输入。', trigger: 'blur' }
  ]
}

const schema = reactive<FormSchema[]>([
  {
    field: 'title',
    colProps: {
      span: 24
    }
  },
  {
    field: 'password',
    label: '新密码',
    component: 'InputPassword',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '50%'
      },
      placeholder: '请输入新密码'
    }
  },
  {
    field: 'password_two',
    label: '再次输入新密码',
    component: 'InputPassword',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '50%'
      },
      placeholder: '请再次输入新密码'
    }
  },
  {
    field: 'save',
    colProps: {
      span: 24
    }
  }
])

const { register, elFormRef, methods } = useForm()

const { setValues } = methods
setValues(authStore.getUser)

const loading = ref(false)

// 提交
const save = async () => {
  const formRef = unref(elFormRef)
  await formRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      const { getFormData } = methods
      const formData = await getFormData()
      try {
        const res = await postCurrentUserResetPassword(formData)
        if (res) {
          formRef.resetFields()
          ElMessage.success('保存成功')
        }
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <Form
    :schema="schema"
    :rules="rules"
    hide-required-asterisk
    class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
    @register="register"
  >
    <template #save>
      <div class="w-[50%]">
        <ElButton :loading="loading" type="primary" class="w-[100%]" @click="save"> 保存 </ElButton>
      </div>
    </template>
  </Form>
</template>

<style lang="less" scoped></style>
