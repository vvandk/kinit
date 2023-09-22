<script setup lang="ts">
import { ElDropdown, ElDropdownMenu, ElDropdownItem, ElMessageBox } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { useDesign } from '@/hooks/web/useDesign'
import LockDialog from './components/LockDialog.vue'
import { ref, computed } from 'vue'
import LockPage from './components/LockPage.vue'
import { useLockStore } from '@/store/modules/lock'
import { useRouter } from 'vue-router'
import avatar from '@/assets/imgs/avatar.jpg'

const lockStore = useLockStore()

const getIsLock = computed(() => lockStore.getLockInfo?.isLock ?? false)

const authStore = useAuthStoreWithOut()

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('user-info')

const { push } = useRouter()

const { t } = useI18n()

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

const dialogVisible = ref<boolean>(false)

// 锁定屏幕
const lockScreen = () => {
  dialogVisible.value = true
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

const user = computed(() => authStore.getUser)
</script>

<template>
  <ElDropdown class="custom-hover" :class="prefixCls" trigger="click">
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
          <div @click="lockScreen">{{ t('lock.lockScreen') }}</div>
        </ElDropdownItem>
        <ElDropdownItem>
          <div @click="loginOut">{{ t('common.loginOut') }}</div>
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>

  <LockDialog v-if="dialogVisible" v-model="dialogVisible" />
  <teleport to="body">
    <transition name="fade-bottom" mode="out-in">
      <LockPage v-if="getIsLock" />
    </transition>
  </teleport>
</template>
