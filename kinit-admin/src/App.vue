<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/store/modules/app'
import { ConfigGlobal } from '@/components/ConfigGlobal'
import { isDark } from '@/utils/is'
import { useDesign } from '@/hooks/web/useDesign'
import { useStorage } from '@/hooks/web/useStorage'
import { getSystemBaseConfigApi } from '@/api/vadmin/system/settings'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('app')

const appStore = useAppStore()

const currentSize = computed(() => appStore.getCurrentSize)

const greyMode = computed(() => appStore.getGreyMode)

const { getStorage } = useStorage()

// 根据浏览器当前主题设置系统主题色
const setDefaultTheme = () => {
  if (getStorage('isDark') !== null) {
    appStore.setIsDark(getStorage('isDark'))
    return
  }
  const isDarkTheme = isDark()
  appStore.setIsDark(isDarkTheme)
}

// 添加mate标签
const addMeta = (name: string, content: string) => {
  const meta = document.createElement('meta')
  meta.content = content
  meta.name = name
  document.getElementsByTagName('head')[0].appendChild(meta)
}

// 获取并设置系统配置
const setSystemConfig = async () => {
  const res = await getSystemBaseConfigApi()
  if (res) {
    appStore.setTitle(res.data.web_title || import.meta.env.VITE_APP_TITLE)
    appStore.setLogoImage(res.data.web_logo || '/media/system/logo.png')
    appStore.setFooterContent(res.data.web_copyright || 'Copyright ©2022-present K')
    appStore.setIcpNumber(res.data.web_icp_number || '')
    addMeta(
      'description',
      res.data.web_desc || 'Kinit 是一套开箱即用的中后台解决方案，可以作为新项目的启动模版。'
    )
  }
}

setDefaultTheme()
setSystemConfig()
</script>

<template>
  <ConfigGlobal :size="currentSize">
    <RouterView :class="greyMode ? `${prefixCls}-grey-mode` : ''" />
  </ConfigGlobal>
</template>

<style lang="less">
@prefix-cls: ~'@{namespace}-app';

.size {
  width: 100% !important;
  height: 100%;
}

html,
body {
  padding: 0 !important;
  margin: 0;
  overflow: hidden;
  .size;

  #app {
    .size;
  }
}

.@{prefix-cls}-grey-mode {
  filter: grayscale(100%);
}

ol {
  display: block;
  list-style-type: decimal;
  margin-block-start: 1em;
  margin-block-end: 1em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  padding-inline-start: 40px;
}
</style>
