<script setup lang="ts">
import { ElButton } from 'element-plus'
import { getSystemSettingsApi, putSystemSettingsApi } from '@/api/vadmin/system/settings'
import { propTypes } from '@/utils/propTypes'
import { Editor, EditorExpose } from '@/components/Editor'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  tabId: propTypes.number
})

const editorRef = ref<typeof Editor & EditorExpose>()

const defaultHtml = ref('')

const getData = async () => {
  const res = await getSystemSettingsApi({ tab_id: props.tabId })
  if (res) {
    defaultHtml.value = res.data.web_privacy || ''
  }
}

const loading = ref(false)

const save = async () => {
  loading.value = true
  try {
    const res = await putSystemSettingsApi({ web_privacy: defaultHtml.value })
    if (res) {
      getData()
      return ElMessage.success('更新成功')
    }
  } finally {
    loading.value = false
  }
}

const editorConfig = {
  customAlert: (s: string, t: string) => {
    switch (t) {
      case 'success':
        ElMessage.success(s)
        break
      case 'info':
        ElMessage.info(s)
        break
      case 'warning':
        ElMessage.warning(s)
        break
      case 'error':
        ElMessage.error(s)
        break
      default:
        ElMessage.info(s)
        break
    }
  },
  autoFocus: true,
  scroll: true,
  readOnly: false,
  uploadImgShowBase64: true
}

getData()
</script>

<template>
  <Editor
    v-model="defaultHtml"
    ref="editorRef"
    editorId="web_privacy"
    :editorConfig="editorConfig"
  />
  <div class="mt-10px" style="float: right">
    <ElButton :loading="loading" type="primary" @click="save">立即保存</ElButton>
  </div>
</template>

<style scoped lang="less"></style>
