<script setup lang="tsx">
import { reactive, ref, watch } from 'vue'
import { Form } from '@/components/Form'
import { useI18n } from '@/hooks/web/useI18n'
import { ElButton, ElCheckbox, ElLink } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
import { getRoleMenusApi } from '@/api/login'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { usePermissionStore } from '@/store/modules/permission'
import { useRouter } from 'vue-router'
import type { RouteLocationNormalizedLoaded, RouteRecordRaw } from 'vue-router'
import { UserLoginType } from '@/api/login/types'
import { useValidator } from '@/hooks/web/useValidator'
import { useStorage } from '@/hooks/web/useStorage'
import { FormSchema } from '@/components/Form'
import { Icon } from '@/components/Icon'

const emit = defineEmits(['to-telephone'])

const { required } = useValidator()

const permissionStore = usePermissionStore()

const authStore = useAuthStoreWithOut()

const { currentRoute, addRoute, push } = useRouter()
const { setStorage } = useStorage()

const { t } = useI18n()

const remember = ref(false)
const hoverColor = 'var(--el-color-primary)'

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
    },
    formItemProps: {
      slots: {
        default: () => {
          return <h2 class="text-2xl font-bold text-center w-[100%]">{t('login.login')}</h2>
        }
      }
    }
  },
  {
    field: 'telephone',
    label: t('login.telephone'),
    value: '15020221010',
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
    hidden: true
  },
  {
    field: 'tool',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="flex justify-between items-center w-[100%]">
                <ElCheckbox v-model={remember.value} label={t('login.remember')} size="small" />
                <ElLink type="primary" underline={false}>
                  {t('login.forgetPassword')}
                </ElLink>
              </div>
            </>
          )
        }
      }
    }
  },
  {
    field: 'login',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="w-[100%]">
                <ElButton loading={loading.value} type="primary" class="w-[100%]" onClick={signIn}>
                  {t('login.login')}
                </ElButton>
              </div>
              <div class="w-[100%] mt-15px">
                <ElButton class="w-[100%]" onClick={toTelephoneLogin}>
                  {t('login.smsLogin')}
                </ElButton>
              </div>
            </>
          )
        }
      }
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
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="flex justify-between w-[100%]">
                <Icon
                  icon="ant-design:github-filled"
                  size={iconSize}
                  class="cursor-pointer ant-icon"
                  color={iconColor}
                  hoverColor={hoverColor}
                />
                <Icon
                  icon="ant-design:wechat-filled"
                  size={iconSize}
                  class="cursor-pointer ant-icon"
                  color={iconColor}
                  hoverColor={hoverColor}
                />
                <Icon
                  icon="ant-design:alipay-circle-filled"
                  size={iconSize}
                  color={iconColor}
                  hoverColor={hoverColor}
                  class="cursor-pointer ant-icon"
                />
                <Icon
                  icon="ant-design:weibo-circle-filled"
                  size={iconSize}
                  color={iconColor}
                  hoverColor={hoverColor}
                  class="cursor-pointer ant-icon"
                />
              </div>
            </>
          )
        }
      }
    }
  }
])

const iconSize = 30
const { formRegister, formMethods } = useForm()
const { getFormData, getElFormExpose } = formMethods
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
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    loading.value = true
    const formData: UserLoginType = await getFormData()
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
}

// 获取用户菜单信息
const getMenu = async () => {
  const res = await getRoleMenusApi()
  if (res) {
    const routers = res.data || []
    setStorage('roleRouters', routers)
    await permissionStore.generateRoutes(routers).catch(() => {})
    permissionStore.getAddRouters.forEach((route) => {
      addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
    })
    permissionStore.setIsAddRouters(true)
    push({ path: redirect.value || permissionStore.addRouters[0].path })
  }
}

// 手机验证码登录
const toTelephoneLogin = () => {
  emit('to-telephone')
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
    @register="formRegister"
  />
</template>
