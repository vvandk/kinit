<script setup lang="ts">
import { onBeforeUnmount, computed, PropType, unref, nextTick, ref, watch, shallowRef } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { IDomEditor, IEditorConfig, i18nChangeLanguage } from '@wangeditor/editor'
import { propTypes } from '@/utils/propTypes'
import { isNumber } from '@/utils/is'
import { ElMessage } from 'element-plus'
import { useLocaleStore } from '@/store/modules/locale'
import { InsertImageType, InsertVideoType } from './types'
import { uploadImageToOSSApi, uploadVideoToOSSApi } from '@/api/vadmin/system/files'

// editor 官方文档：https://www.wangeditor.com/v5/getting-started.html

const localeStore = useLocaleStore()

const currentLocale = computed(() => localeStore.getCurrentLocale)

i18nChangeLanguage(unref(currentLocale).lang)

const props = defineProps({
  editorId: propTypes.string.def('wangeEditor-1'),
  height: propTypes.oneOfType([Number, String]).def('500px'),
  editorConfig: {
    type: Object as PropType<IEditorConfig>,
    default: () => undefined
  },
  modelValue: propTypes.string.def('')
})

const emit = defineEmits(['change', 'update:modelValue'])

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef<IDomEditor>()

const valueHtml = ref('')

watch(
  () => props.modelValue,
  (val: string) => {
    if (val === unref(valueHtml)) return
    valueHtml.value = val
  },
  {
    immediate: true
  }
)

// 监听
watch(
  () => valueHtml.value,
  (val: string) => {
    emit('update:modelValue', val)
  }
)

const handleCreated = (editor: IDomEditor) => {
  editorRef.value = editor
}

// 编辑器配置
const editorConfig = computed((): IEditorConfig => {
  return Object.assign(
    {
      readOnly: false,
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
      autoFocus: false,
      scroll: true,
      uploadImgShowBase64: true,
      MENU_CONF: {
        uploadImage: {
          // 自定义上传图片
          // 官方文档：https://www.wangeditor.com/v5/menu-config.html#%E8%87%AA%E5%AE%9A%E4%B9%89%E4%B8%8A%E4%BC%A0
          async customUpload(file: File, insertFn: InsertImageType) {
            // 上传图片前的检查
            if (!['image/jpeg', 'image/gif', 'image/png'].includes(file.type)) {
              return ElMessage.error(`${file.name}上传失败：上传图片只能是 JPG/GIF/PNG/ 格式!`)
            }
            if (!(file.size / 1024 / 1024 < 2)) {
              return ElMessage.error(`${file.name}上传失败：上传图片大小不能超过 2MB!`)
            }

            // 自己实现上传，并得到图片 url
            const formData = new FormData()
            formData.append('file', file)
            formData.append('path', 'editor/image')
            const res = await uploadImageToOSSApi(formData)
            insertFn(res.data, '', res.data)
          }
        },
        uploadVideo: {
          // 自定义上传视频
          // 官方文档：https://www.wangeditor.com/v5/menu-config.html#%E8%87%AA%E5%AE%9A%E4%B9%89%E5%8A%9F%E8%83%BD-1
          async customUpload(file: File, insertFn: InsertVideoType) {
            // 上传视频前的检查
            if (!['video/mp4', 'video/mpeg'].includes(file.type)) {
              return ElMessage.error(`${file.name}上传失败：上传视频只能是 mp4/mpeg/ 格式!`)
            }
            if (!(file.size / 1024 / 1024 < 5)) {
              return ElMessage.error(`${file.name}上传失败：上传视频大小不能超过 5MB!`)
            }
            // 自己实现上传，并得到视频 url
            const formData = new FormData()
            formData.append('file', file)
            formData.append('path', 'editor/video')
            const res = await uploadVideoToOSSApi(formData)
            insertFn(res.data, '')
          }
        }
      }
    },
    props.editorConfig || {}
  )
})

const editorStyle = computed(() => {
  return {
    height: isNumber(props.height) ? `${props.height}px` : props.height
  }
})

// 回调函数
const handleChange = (editor: IDomEditor) => {
  emit('change', editor)
}

// 组件销毁时，及时销毁编辑器
onBeforeUnmount(() => {
  const editor = unref(editorRef.value)

  // 销毁，并移除 editor
  editor?.destroy()
})

const getEditorRef = async (): Promise<IDomEditor> => {
  await nextTick()
  return unref(editorRef.value) as IDomEditor
}

defineExpose({
  getEditorRef
})
</script>

<template>
  <div class="border-1 border-solid border-[var(--el-border-color)] z-10">
    <!-- 工具栏 -->
    <Toolbar
      :editor="editorRef"
      :editorId="editorId"
      class="border-0 b-b-1 border-solid border-[var(--el-border-color)]"
    />
    <!-- 编辑器 -->
    <Editor
      v-model="valueHtml"
      :editorId="editorId"
      :defaultConfig="editorConfig"
      :style="editorStyle"
      @on-change="handleChange"
      @on-created="handleCreated"
    />
  </div>
</template>

<style src="@wangeditor/editor/dist/css/style.css"></style>
