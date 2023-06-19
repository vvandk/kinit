<script setup lang="ts">
import { Form } from '@/components/Form'
import { reactive, ref, unref, watch } from 'vue'
import { useI18n } from '@/hooks/web/useI18n'
import { useForm } from '@/hooks/web/useForm'
import { ElButton, ElInput, FormRules, ElDivider, ElMessage } from 'element-plus'
import { useValidator } from '@/hooks/web/useValidator'
import { FormSchema } from '@/types/form'
import { postSMSCodeApi } from '@/api/login'
import { UserLoginType } from '@/api/login/types'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { RouteLocationNormalizedLoaded, useRouter, RouteRecordRaw } from 'vue-router'
import { getRoleMenusApi } from '@/api/login'
import { useCache } from '@/hooks/web/useCache'
import { useRouterStore } from '@/store/modules/router'

const emit = defineEmits(['to-login'])

const { register, elFormRef, methods } = useForm()
const { t } = useI18n()
const { required } = useValidator()
const { currentRoute, addRoute, push } = useRouter()
const routerStore = useRouterStore()

const schema = reactive<FormSchema[]>([
  {
    field: 'title',
    colProps: {
      span: 24
    }
  },
  {
    field: 'telephone',
    label: t('login.telephone'),
    value: '',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: t('login.telephonePlaceholder'),
      maxlength: 11
    }
  },
  {
    field: 'password',
    label: '短信验证码',
    colProps: {
      span: 24
    }
  },
  {
    field: 'method',
    label: '登录类型',
    value: '1',
    component: 'Input',
    ifshow: () => false
  },
  {
    field: 'login',
    colProps: {
      span: 24
    }
  }
])

const rules: FormRules = {
  telephone: [required()],
  method: [required()],
  password: [required()]
}

const toLogin = () => {
  emit('to-login')
}

const loading = ref(false)

const redirect = ref<string>('')

watch(
  () => currentRoute.value,
  (route: RouteLocationNormalizedLoaded) => {
    redirect.value = route?.query?.redirect as string
  },
  {
    immediate: true
  }
)

const telephoneCodeLogin = async () => {
  const formRef = unref(elFormRef)
  await formRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      const { getFormData } = methods
      const formData = await getFormData<UserLoginType>()
      const authStore = useAuthStoreWithOut()
      try {
        const res = await authStore.login(formData)
        if (res) {
          if (!res.data.is_reset_password) {
            // 重置密码
            push({ path: '/reset/password' })
          } else {
            // 是否使用动态路由
            getMenu()
          }
        } else {
          loading.value = false
        }
      } catch (e: any) {
        loading.value = false
      }
    }
  })
}

let SMSCodeStatus = ref(true)
let SMSCodeNumber = ref(60)

const getSMSCode = async () => {
  const formRef = unref(elFormRef)
  await formRef?.validateField('telephone', async (isValid) => {
    if (isValid) {
      SMSCodeStatus.value = false
      SMSCodeNumber.value = 60
      const { getFormData } = methods
      const formData = await getFormData<UserLoginType>()
      try {
        const res = await postSMSCodeApi({ telephone: formData.telephone })
        if (res?.data) {
          let timer = setInterval(() => {
            SMSCodeNumber.value--
            if (SMSCodeNumber.value < 1) {
              SMSCodeStatus.value = true
              clearInterval(timer)
            }
          }, 1000)
        } else {
          ElMessage.error('发送失败，请联系管理员')
          SMSCodeStatus.value = true
        }
      } catch (e: any) {
        SMSCodeStatus.value = true
      }
    }
  })
}

// 获取用户菜单信息
const getMenu = async () => {
  const res = await getRoleMenusApi()
  if (res) {
    const { wsCache } = useCache()
    const routers = res.data || []
    wsCache.set('roleRouters', routers)
    await routerStore.generateRoutes(routers).catch(() => {})
    routerStore.getAddRouters.forEach((route) => {
      addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
    })
    routerStore.setIsAddRouters(true)
    push({ path: redirect.value || routerStore.addRouters[0].path })
  }
}
</script>

<template>
  <Form
    :schema="schema"
    :rules="rules"
    label-position="top"
    hide-required-asterisk
    size="large"
    class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
    @register="register"
  >
    <template #title>
      <h2 class="text-2xl font-bold text-center w-[100%]">短信验证码登录</h2>
    </template>

    <template #password="form">
      <div class="w-[100%] flex">
        <ElInput v-model="form['password']" placeholder="请输入短信验证码">
          <template #suffix>
            <ElDivider direction="vertical" />
            <el-button v-if="SMSCodeStatus" type="primary" link @click="getSMSCode">
              获取验证码
            </el-button>
            <el-button v-else type="primary" :disabled="!SMSCodeStatus" link>
              {{ SMSCodeNumber }}S后再试
            </el-button>
          </template>
        </ElInput>
      </div>
    </template>

    <template #login>
      <div class="w-[100%]">
        <ElButton type="primary" class="w-[100%]" :loading="loading" @click="telephoneCodeLogin">
          {{ t('login.login') }}
        </ElButton>
      </div>
      <div class="w-[100%] mt-15px">
        <ElButton class="w-[100%]" @click="toLogin"> 密码登录 </ElButton>
      </div>
    </template>
  </Form>
</template>
