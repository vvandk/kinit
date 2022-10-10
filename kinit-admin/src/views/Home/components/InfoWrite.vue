<script setup lang="ts">
import { reactive, unref, ref } from 'vue'
import { Form } from '@/components/Form'
import { ElButton } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
import { postCurrentUserUpdateInfo } from '@/api/vadmin/auth/user'
import { useValidator } from '@/hooks/web/useValidator'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { ElMessage } from 'element-plus'

const { required } = useValidator()

const authStore = useAuthStoreWithOut()

const rules = {
  name: [required()],
  gender: [required()]
}

const schema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '用户名称',
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
    field: 'gender',
    label: '性别',
    colProps: {
      span: 24
    },
    component: 'Radio',
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
        const res = await postCurrentUserUpdateInfo(formData)
        if (res) {
          authStore.updateUser(res.data)
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
