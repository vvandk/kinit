<script setup lang="ts">
import { reactive, ref, unref, watch } from 'vue'
import { Form } from '@/components/Form'
import { useI18n } from '@/hooks/web/useI18n'
import { ElButton, ElCheckbox, ElLink } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
import { getRoleMenusApi } from '@/api/login'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { useRouterStore } from '@/store/modules/router'
import { useRouter } from 'vue-router'
import type { RouteLocationNormalizedLoaded, RouteRecordRaw } from 'vue-router'
import { UserLoginType } from '@/api/login/types'
import { useValidator } from '@/hooks/web/useValidator'
import { useCache } from '@/hooks/web/useCache'
import { FormSchema } from '@/types/form'

const emit = defineEmits(['to-telephone-code'])

const { required } = useValidator()

const routerStore = useRouterStore()

const { currentRoute, addRoute, push } = useRouter()

const { t } = useI18n()

const rules = {
  telephone: [required()],
  method: [required()],
  password: [required()]
}

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
    value: '15020221010',
    // value: '15000000006',
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
    label: t('login.password'),
    value: 'kinit2022',
    // value: '000006',
    component: 'InputPassword',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: t('login.passwordPlaceholder')
    }
  },
  {
    field: 'method',
    label: '登录类型',
    value: '0',
    component: 'Input',
    ifshow: () => false
  },
  {
    field: 'tool',
    colProps: {
      span: 24
    }
  },
  {
    field: 'login',
    colProps: {
      span: 24
    }
  },
  {
    field: 'other',
    component: 'Divider',
    label: t('login.otherLogin'),
    componentProps: {
      contentPosition: 'center'
    }
  },
  {
    field: 'otherIcon',
    colProps: {
      span: 24
    }
  }
])

const iconSize = 30
const remember = ref(false)
const { register, elFormRef, methods } = useForm()
const loading = ref(false)
const iconColor = '#999'
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

// 登录
const signIn = async () => {
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
            // 获取动态路由
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

// 手机验证码登录
const toTelephoneSignIn = () => {
  emit('to-telephone-code')
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
      <h2 class="text-2xl font-bold text-center w-[100%]">{{ t('login.login') }}</h2>
    </template>

    <template #tool>
      <div class="flex justify-between items-center w-[100%]">
        <ElCheckbox v-model="remember" :label="t('login.remember')" size="small" />
        <ElLink type="primary" :underline="false">{{ t('login.forgetPassword') }}</ElLink>
      </div>
    </template>

    <template #login>
      <div class="w-[100%]">
        <ElButton :loading="loading" type="primary" class="w-[100%]" @click="signIn">
          {{ t('login.login') }}
        </ElButton>
      </div>
      <div class="w-[100%] mt-15px">
        <ElButton class="w-[100%]" @click="toTelephoneSignIn"> 短信验证码登录 </ElButton>
      </div>
    </template>

    <template #otherIcon>
      <div class="flex justify-between w-[100%]">
        <Icon
          icon="ant-design:github-filled"
          :size="iconSize"
          class="cursor-pointer anticon"
          :color="iconColor"
        />
        <Icon
          icon="ant-design:wechat-filled"
          :size="iconSize"
          class="cursor-pointer anticon"
          :color="iconColor"
        />
        <Icon
          icon="ant-design:alipay-circle-filled"
          :size="iconSize"
          :color="iconColor"
          class="cursor-pointer anticon"
        />
        <Icon
          icon="ant-design:weibo-circle-filled"
          :size="iconSize"
          :color="iconColor"
          class="cursor-pointer anticon"
        />
      </div>
    </template>
  </Form>
</template>

<style lang="less" scoped>
:deep(.anticon) {
  &:hover {
    color: var(--el-color-primary) !important;
  }
}
</style>
