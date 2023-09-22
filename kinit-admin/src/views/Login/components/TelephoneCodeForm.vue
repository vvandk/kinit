<script setup lang="tsx">
import { Form } from '@/components/Form'
import { reactive, ref, watch } from 'vue'
import { useI18n } from '@/hooks/web/useI18n'
import { useForm } from '@/hooks/web/useForm'
import { ElButton, ElInput, FormRules, ElDivider, ElMessage } from 'element-plus'
import { useValidator } from '@/hooks/web/useValidator'
import { FormSchema } from '@/components/Form'
import { postSMSCodeApi } from '@/api/login'
import { UserLoginType } from '@/api/login/types'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { RouteLocationNormalizedLoaded, useRouter, RouteRecordRaw } from 'vue-router'
import { getRoleMenusApi } from '@/api/login'
import { useStorage } from '@/hooks/web/useStorage'
import { usePermissionStore } from '@/store/modules/permission'

const emit = defineEmits(['to-password'])

const { formRegister, formMethods } = useForm()
const { getFormData, getElFormExpose } = formMethods
const { t } = useI18n()
const { required } = useValidator()
const { currentRoute, addRoute, push } = useRouter()
const permissionStore = usePermissionStore()
const authStore = useAuthStoreWithOut()
const { setStorage } = useStorage()

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
    label: t('login.SMSCode'),
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: (data) => {
          return (
            <div class="w-[100%] flex">
              <ElInput
                v-model={data['password']}
                placeholder={t('login.codePlaceholder')}
                v-slots={{
                  suffix: () => (
                    <>
                      <ElDivider direction="vertical" />
                      {SMSCodeStatus.value ? (
                        <ElButton type="primary" link onClick={getSMSCode}>
                          {t('login.getSMSCode')}
                        </ElButton>
                      ) : (
                        <ElButton type="primary" disabled={!SMSCodeStatus.value} link>
                          {SMSCodeNumber.value + t('login.SMSCodeRetry')}
                        </ElButton>
                      )}
                    </>
                  )
                }}
              ></ElInput>
            </div>
          )
        }
      }
    }
  },
  {
    field: 'method',
    label: '登录类型',
    value: '1',
    component: 'Input',
    hidden: true
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
            <div class="w-[100%]">
              <div class="w-[100%]">
                <ElButton
                  type="primary"
                  class="w-[100%]"
                  loading={loading.value}
                  onClick={telephoneCodeLogin}
                >
                  {t('login.login')}
                </ElButton>
              </div>
              <div class="w-[100%] mt-15px">
                <ElButton class="w-[100%]" onClick={toPasswordLogin}>
                  {t('login.passwordLogin')}
                </ElButton>
              </div>
            </div>
          )
        }
      }
    }
  }
])

const rules: FormRules = {
  telephone: [required()],
  method: [required()],
  password: [required()]
}

const toPasswordLogin = () => {
  emit('to-password')
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
}

let SMSCodeStatus = ref(true)
let SMSCodeNumber = ref(60)

const getSMSCode = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validateField('telephone')
  if (valid) {
    SMSCodeStatus.value = false
    SMSCodeNumber.value = 60
    const formData: UserLoginType = await getFormData()
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
