<script setup lang="ts">
import { reactive, unref, ref, watch } from 'vue'
import { Form } from '@/components/Form'
import { ElButton } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
import { postCurrentUserResetPassword } from '@/api/vadmin/auth/user'
import { usePermissionStore } from '@/store/modules/permission'
import { useRouter } from 'vue-router'
import type { RouteRecordRaw, RouteLocationNormalizedLoaded } from 'vue-router'
import { getRoleMenusApi } from '@/api/login'
import { useValidator } from '@/hooks/web/useValidator'
import { useCache } from '@/hooks/web/useCache'
import { useAppStore } from '@/store/modules/app'
import { Footer } from '@/components/Footer'
import { computed } from 'vue'

const appStore = useAppStore()

const { required } = useValidator()

const footer = computed(() => appStore.getFooter)

const permissionStore = usePermissionStore()

const { addRoute, push, currentRoute } = useRouter()

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
  },
  {
    field: 'reset',
    colProps: {
      span: 24
    }
  }
])

const { register, elFormRef, methods } = useForm()

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
  const formRef = unref(elFormRef)
  await formRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      const { getFormData } = methods
      const formData = await getFormData()
      try {
        const res = await postCurrentUserResetPassword(formData)
        if (res) {
          // 是否使用动态路由
          getMenu()
        }
      } finally {
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
          <h2 class="text-2xl font-bold text-center w-[100%]">第一次登录系统，需先重置密码</h2>
        </template>

        <template #reset>
          <div class="w-[100%]">
            <ElButton :loading="loading" type="primary" class="w-[100%]" @click="save">
              重置密码
            </ElButton>
          </div>
        </template>
      </Form>
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
  width: 100%;
}
</style>
