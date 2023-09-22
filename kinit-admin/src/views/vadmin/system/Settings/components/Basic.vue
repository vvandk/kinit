<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { ElButton, ElUpload } from 'element-plus'
import { getSystemSettingsApi, putSystemSettingsApi } from '@/api/vadmin/system/settings'
import { reactive, ref } from 'vue'
import { ElMessage, ElIcon } from 'element-plus'
import type { UploadProps } from 'element-plus'
import { useStorage } from '@/hooks/web/useStorage'
import { useAppStore } from '@/store/modules/app'
import { propTypes } from '@/utils/propTypes'
import { Icon } from '@/components/Icon'
import { useValidator } from '@/hooks/web/useValidator'

const { required } = useValidator()
const { getStorage } = useStorage()
const appStore = useAppStore()

const props = defineProps({
  tabId: propTypes.number
})

const token = getStorage(appStore.getToken)

const formSchema = reactive<FormSchema[]>([
  {
    field: 'web_title',
    label: '系统标题',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'web_logo',
    label: '系统 LOGO',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: (data) => {
          const beforeImageUpload: UploadProps['beforeUpload'] = (rawFile) => {
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

          // 上传成功的钩子函数
          const handleUploadSuccess: UploadProps['onSuccess'] = (response) => {
            if (response.code === 200) {
              // setValue('web_logo', response.data.remote_path)
              data.web_logo = response.data.remote_path
            } else {
              ElMessage.error(response.message)
            }
          }
          return (
            <ElUpload
              class="system-settings-basic-image-uploader"
              action="/api/vadmin/system/upload/image/to/local"
              data={{ path: 'system' }}
              show-file-list={false}
              before-upload={beforeImageUpload}
              on-success={handleUploadSuccess}
              accept="image/jpeg,image/gif,image/png"
              name="file"
              headers={{ Authorization: token }}
            >
              {data.web_logo ? (
                <img src={data.web_logo} class="logo-image" />
              ) : (
                <ElIcon class="logo-image-uploader-icon">
                  <Icon icon="akar-icons:plus" size={23} />
                </ElIcon>
              )}
            </ElUpload>
          )
        }
      }
    }
  },
  {
    field: 'web_desc',
    label: '系统描述',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      rows: 4,
      type: 'textarea',
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'web_ico',
    label: 'ICO 图标',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: (data) => {
          const beforeImageUpload: UploadProps['beforeUpload'] = (rawFile) => {
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

          // 上传成功的钩子函数
          const handleUploadSuccess: UploadProps['onSuccess'] = (response) => {
            if (response.code === 200) {
              // setValue('web_ico', response.data.remote_path)
              // setValue('web_ico_local_path', response.data.local_path)
              data.web_ico = response.data.remote_path
              data.web_ico_local_path = response.data.local_path
            } else {
              ElMessage.error(response.message)
            }
          }
          return (
            <ElUpload
              class="system-settings-basic-image-uploader"
              action="/api/vadmin/system/upload/image/to/local"
              data={{ path: 'system' }}
              show-file-list={false}
              before-upload={beforeImageUpload}
              on-success={handleUploadSuccess}
              accept="image/jpeg,image/gif,image/png"
              name="file"
              headers={{ Authorization: token }}
            >
              {data.web_ico ? (
                <img src={data.web_ico} class="ico-image" />
              ) : (
                <ElIcon class="ico-image-uploader-icon">
                  <Icon icon="akar-icons:plus" size={23} />
                </ElIcon>
              )}
            </ElUpload>
          )
        }
      }
    }
  },
  {
    field: 'web_ico_local_path',
    label: 'ICO 图标服务器文件地址',
    component: 'Input',
    colProps: {
      span: 24
    },
    hidden: true
  },
  {
    field: 'web_icp_number',
    label: '备案号',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'web_copyright',
    label: '版权信息',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'active',
    label: '',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <ElButton loading={loading.value} type="primary" onClick={save}>
                立即提交
              </ElButton>
            </>
          )
        }
      }
    }
  }
])

const rules = reactive({
  web_title: [required()],
  web_logo: [required()],
  web_ico: [required()]
})

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

let formData = ref({} as Recordable)

const getData = async () => {
  const res = await getSystemSettingsApi({ tab_id: props.tabId })
  if (res) {
    await setValues(res.data)
    formData.value = res.data
    const elForm = await getElFormExpose()
    elForm?.clearValidate()
  }
}

const loading = ref(false)

const save = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await getFormData()
    loading.value = true
    if (!formData) {
      loading.value = false
      return ElMessage.error('未获取到数据')
    }
    try {
      const res = await putSystemSettingsApi(formData)
      if (res) {
        appStore.setTitle(res.data.web_title || import.meta.env.VITE_APP_TITLE)
        appStore.setLogoImage(res.data.web_logo || '/static/system/logo.png')
        appStore.setFooterContent(res.data.web_copyright || 'Copyright ©2022-present K')
        appStore.setIcpNumber(res.data.web_icp_number || '')
        return ElMessage.success('更新成功')
      }
    } finally {
      loading.value = false
    }
  }
}

getData()
</script>

<template>
  <Form :rules="rules" @register="formRegister" :schema="formSchema" />
</template>

<style lang="less">
.system-settings-basic-image-uploader {
  .logo-image {
    width: 178px;
    height: 178px;
    display: block;
  }

  .ico-image {
    width: 100px;
    height: 100px;
    display: block;
  }

  .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
  }

  .el-upload:hover {
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
}
</style>
