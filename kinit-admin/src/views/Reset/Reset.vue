<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { computed, reactive, ref, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { ElButton, ElMessage } from 'element-plus'
import { postCurrentUserResetPassword } from '@/api/vadmin/auth/user'
import { getRoleMenusApi } from '@/api/login'
import { useStorage } from '@/hooks/web/useStorage'
import { usePermissionStore } from '@/store/modules/permission'
import { RouteLocationNormalizedLoaded, RouteRecordRaw, useRouter } from 'vue-router'
import { useAppStore } from '@/store/modules/app'
import { Footer } from '@/components/Footer'

const { required } = useValidator()
const { setStorage } = useStorage()
const { addRoute, push, currentRoute } = useRouter()

const authStore = useAuthStoreWithOut()
const appStore = useAppStore()
const permissionStore = usePermissionStore()

const footer = computed(() => appStore.getFooter)

const formSchema = reactive<FormSchema[]>([
  {
    field: 'password',
    label: '新密码',
    component: 'InputPassword',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
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
        width: '100%'
      },
      placeholder: '请再次输入新密码'
    }
  }
])

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

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

setValues(authStore.getUser)

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
      const res = await postCurrentUserResetPassword(formData)
      if (res) {
        // 是否使用动态路由
        getMenu()
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
</script>

<template>
  <div class="main-container">
    <div class="form-container">
      <div>
        <h2 class="text-2xl font-bold text-center w-[100%]">第一次登录系统，需先重置密码</h2>
      </div>
      <Form
        @register="formRegister"
        :schema="formSchema"
        :rules="rules"
        hide-required-asterisk
        class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
      />
      <div class="w-[100%]">
        <ElButton :loading="loading" type="primary" class="w-[100%]" @click="save">
          重置密码
        </ElButton>
      </div>
    </div>

    <div class="footer-container">
      <Footer v-if="footer" />
    </div>
  </div>
</template>

<style lang="less" scoped>
:deep(.anticon) {
  &:hover {
    color: var(--el-color-primary) !important;
  }
}

.main-container {
  display: flex;
  flex-direction: column;
  padding-top: 20px;
  width: 100%;
  height: 100%;
  background-color: var(--app-content-bg-color);
  position: relative;
}

.main-container .form-container {
  width: 500px;
  align-self: center;
  padding: 30px;
  background-color: #fff;
  border-radius: 30px;
}

.footer-container {
  position: absolute;
  bottom: 0;
  margin-bottom: 20px;
  width: 100%;
}
</style>
