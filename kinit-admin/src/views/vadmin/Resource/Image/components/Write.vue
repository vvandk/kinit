<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, ref, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { ElUpload, ElImageViewer, ElMessage } from 'element-plus'
import type {
  UploadProps,
  UploadUserFile,
  UploadRequestOptions,
  UploadFile,
  UploadFiles
} from 'element-plus'
import { Icon } from '@/components/Icon'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'upload_method',
    label: '上传方式',
    colProps: {
      span: 24
    },
    component: 'RadioGroup',
    componentProps: {
      options: [
        {
          label: '同时上传',
          value: '1'
        },
        {
          label: '按顺序上传',
          value: '2'
        }
      ]
    },
    value: '1',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'images',
    label: '',
    colProps: {
      span: 24
    },
    formItemProps: {
      rules: [required()],
      slots: {
        default: () => {
          return (
            <>
              <div class="flex justify-between w-[100%]">
                <span>图片资源</span>
                <span>
                  最大数量限制：{fileList.value.length}/{maxLimit.value}
                </span>
              </div>
              <ElUpload
                class="resource-image-uploader"
                action="#"
                http-request={handleHttpRequest}
                v-model:file-list={fileList.value}
                show-file-list={true}
                multiple={true}
                before-upload={beforeImageUpload}
                on-success={handleUploadSuccess}
                on-preview={handlePictureCardPreview}
                on-exceed={handleExceedLimit}
                accept="image/jpeg,image/png"
                name="file"
                list-type="picture-card"
                limit={maxLimit.value}
                drag={true}
                disabled={maxLimit.value <= fileList.value.length}
              >
                {fileList.value.length < maxLimit.value ? (
                  <div class="resource-image-uploader-icon">
                    <Icon icon="akar-icons:plus" size={23} />
                    <span class="text-[12px]">点击或拖拽到这里</span>
                    <span class="text-[12px]">
                      {fileList.value.length}/{maxLimit.value}
                    </span>
                  </div>
                ) : (
                  <div class="resource-image-uploader-icon">
                    <span class="text-[12px]">已到最大限制</span>
                    <span class="text-[12px]">
                      {fileList.value.length}/{maxLimit.value}
                    </span>
                  </div>
                )}
              </ElUpload>
            </>
          )
        }
      }
    }
  }
])

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose, setValue } = formMethods

const dialogVisible = ref(false)
const imgIndex = ref(0)
const maxLimit = ref(50)
const fileList = ref<UploadUserFile[]>([])

const beforeImageUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const isIMAGE = ['image/jpeg', 'image/gif', 'image/png'].includes(rawFile.type)
  const isLtSize = rawFile.size / 1024 / 1024 < 3

  if (!isIMAGE) {
    ElMessage.error('上传图片素材必须是 JPG/PNG/ 格式!')
  }
  if (!isLtSize) {
    ElMessage.error('上传图片素材大小不能超过 3MB!')
  }

  return isIMAGE && isLtSize
}

// 上传成功的钩子函数
const handleUploadSuccess: UploadProps['onSuccess'] = (
  response: any,
  uploadFile: UploadFile,
  uploadFiles: UploadFiles
) => {
  fileList.value = uploadFiles
  setValue('images', uploadFiles)
}

// 自定义上传
const handleHttpRequest: UploadProps['httpRequest'] = (options: UploadRequestOptions) => {
  return new Promise((resolve) => {
    resolve(options)
  })
}

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile: UploadFile) => {
  imgIndex.value = fileList.value.findIndex((item) => item.uid === uploadFile.uid)
  dialogVisible.value = true
}

const handleCloseViewer = () => {
  dialogVisible.value = false
}

const handleExceedLimit = () => {
  ElMessage.error('上传失败，超出图片最大数量限制!')
}

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await getFormData()
    return formData
  }
}

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    setValues(currentRow)
  },
  {
    deep: true,
    immediate: true
  }
)

defineExpose({
  submit
})
</script>

<template>
  <Form @register="formRegister" :schema="formSchema" />

  <ElImageViewer
    v-if="dialogVisible"
    :z-index="9999"
    @close="handleCloseViewer"
    :url-list="fileList.map((item) => item.url as string)"
    :initial-index="imgIndex"
  />
</template>

<style lang="less">
.resource-image-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);

  .el-upload-dragger {
    padding: 0;
  }

  .resource-image-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 148px;
    height: 148px;
    text-align: center;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: center;
  }
}

.resource-image-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}
</style>
