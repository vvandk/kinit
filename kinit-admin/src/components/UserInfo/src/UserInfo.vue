<script setup lang="ts">
import { ElDropdown, ElDropdownMenu, ElDropdownItem, ElMessageBox, ElButton } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { useRouter } from 'vue-router'
import { useDesign } from '@/hooks/web/useDesign'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import avatar from '@/assets/imgs/avatar.jpg'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('user-info')

const { t } = useI18n()

const authStore = useAuthStoreWithOut()

const { push } = useRouter()

const loginOut = () => {
  ElMessageBox.confirm(t('common.loginOutMessage'), t('common.reminder'), {
    confirmButtonText: t('common.ok'),
    cancelButtonText: t('common.cancel'),
    type: 'warning'
  })
    .then(() => {
      authStore.logout()
    })
    .catch(() => {})
}

const toHome = () => {
  push('/home')
}

const toGitee = () => {
  window.open('https://gitee.com/ktianc/kinit')
}

const toGithub = () => {
  window.open('https://github.com/vvandk/kinit')
}

const user = authStore.getUser
</script>

<template>
  <ElDropdown :class="prefixCls" trigger="click">
    <div class="flex items-center">
      <img
        :src="user.avatar ? user.avatar : avatar"
        alt=""
        class="w-[calc(var(--logo-height)-25px)] rounded-[50%]"
      />
      <span class="<lg:hidden text-14px pl-[5px] text-[var(--top-header-text-color)]">{{
        user.name
      }}</span>
    </div>
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem>
          <ElButton @click="toHome" link>个人主页</ElButton>
        </ElDropdownItem>
        <ElDropdownItem>
          <ElButton @click="toGitee" link>Gitee</ElButton>
        </ElDropdownItem>
        <ElDropdownItem>
          <ElButton @click="toGithub" link>Github</ElButton>
        </ElDropdownItem>
        <ElDropdownItem divided>
          <ElButton @click="loginOut" link>退出系统</ElButton>
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>
