<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { schema } from './components/basic.data'
import { ElButton, ElUpload } from 'element-plus'
import { getSystemSettingsApi, putSystemSettingsApi } from '@/api/vadmin/system/settings'
import { ref, unref } from 'vue'
import { ElMessage, ElIcon } from 'element-plus'
import type { UploadProps } from 'element-plus'
import { useCache } from '@/hooks/web/useCache'
import { useAppStore } from '@/store/modules/app'
import { propTypes } from '@/utils/propTypes'

const props = defineProps({
  tabId: propTypes.number
})

const beforeLogoImageUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const isIMAGE = ['image/jpeg', 'image/gif', 'image/png'].includes(rawFile.type)
  const isLtSize = rawFile.size / 1024 / 1024 < 5

  if (!isIMAGE) {
    ElMessage.error('上传LOGO图片必须是 JPG/GIF/PNG/ 格式!')
  }
  if (!isLtSize) {
    ElMessage.error('上传LOGO图片大小不能超过 5MB!')
  }
  return isIMAGE && isLtSize
}

const beforeICOImageUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const isIMAGE = ['image/x-icon'].includes(rawFile.type)
  const isLtSize = rawFile.size / 1024 / 1024 < 2

  if (!isIMAGE) {
    ElMessage.error('上传ICO图标必须是 ico 格式!')
  }
  if (!isLtSize) {
    ElMessage.error('上传ICO图标大小不能超过 2MB!')
  }
  return isIMAGE && isLtSize
}

const { register, methods, elFormRef } = useForm({
  schema: schema
})

const { setValues, setValue } = methods

// 上传成功的钩子函数
const handleICOUploadSuccess: UploadProps['onSuccess'] = (response) => {
  if (response.code === 200) {
    setValue('web_ico', response.data.remote_path)
    setValue('web_ico_local_path', response.data.local_path)
  } else {
    ElMessage.error(response.message)
  }
}

// 上传成功的钩子函数
const handleLogoUploadSuccess: UploadProps['onSuccess'] = (response) => {
  if (response.code === 200) {
    setValue('web_logo', response.data.remote_path)
  } else {
    ElMessage.error(response.message)
  }
}

let formData = ref({} as Recordable)

const getData = async () => {
  const res = await getSystemSettingsApi({ tab_id: props.tabId })
  if (res) {
    setValues(res.data)
    formData.value = res.data
  }
}

const appStore = useAppStore()
const { wsCache } = useCache()
const loading = ref(false)

const token = wsCache.get(appStore.getToken)

const save = async () => {
  const formRef = unref(elFormRef)
  await formRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      let data = await methods.getFormData()
      if (!data) {
        loading.value = false
        return ElMessage.error('未获取到数据')
      }
      try {
        const res = await putSystemSettingsApi(data)
        if (res) {
          appStore.setTitle(data.web_title || import.meta.env.VITE_APP_TITLE)
          appStore.setLogoImage(data.web_logo || '/static/system/logo.png')
          appStore.setFooterContent(data.web_copyright || 'Copyright ©2022-present K')
          appStore.setIcpNumber(data.web_icp_number || '')
          return ElMessage.success('更新成功')
        }
      } finally {
        loading.value = false
      }
    }
  })
}

getData()
</script>

<template>
  <Form @register="register">
    <template #web_logo="form">
      <ElUpload
        class="main-image-uploader"
        action="/api/vadmin/system/upload/image/to/local"
        :data="{ path: 'system' }"
        :show-file-list="false"
        :before-upload="beforeLogoImageUpload"
        :on-success="handleLogoUploadSuccess"
        accept="image/jpeg,image/gif,image/png"
        name="file"
        :headers="{ Authorization: token }"
      >
        <img v-if="form.web_logo" :src="form.web_logo" class="logo-image" />
        <ElIcon v-else class="logo-image-uploader-icon"
          ><Icon icon="akar-icons:plus" :size="23"
        /></ElIcon>
      </ElUpload>
    </template>

    <template #web_ico="form">
      <ElUpload
        class="main-image-uploader"
        action="/api/vadmin/system/upload/image/to/local"
        :data="{ path: 'system' }"
        :show-file-list="false"
        :before-upload="beforeICOImageUpload"
        :on-success="handleICOUploadSuccess"
        accept="image/x-icon"
        name="file"
        :headers="{ Authorization: token }"
      >
        <img v-if="form.web_ico" :src="form.web_ico" class="ico-image" />
        <ElIcon v-else class="ico-image-uploader-icon"
          ><Icon icon="akar-icons:plus" :size="23"
        /></ElIcon>
      </ElUpload>
    </template>

    <template #active>
      <ElButton type="primary" @click="save">立即提交</ElButton>
    </template>
  </Form>
</template>

<style scoped lang="less">
.main-image-uploader .logo-image {
  width: 178px;
  height: 178px;
  display: block;
}

.main-image-uploader .ico-image {
  width: 100px;
  height: 100px;
  display: block;
}
</style>

<style lang="less">
.main-image-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.main-image-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.logo-image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}

.el-icon.ico-image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
}
</style>
