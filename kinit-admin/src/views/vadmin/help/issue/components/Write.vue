<script lang="ts">
export default {
  name: 'HelpIssueForm'
}
</script>

<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { ref, unref, reactive } from 'vue'
import { schema } from './issue.data'
import { ContentWrap } from '@/components/ContentWrap'
import { ElMessage, ElButton } from 'element-plus'
import { Editor, EditorExpose } from '@/components/Editor'
import { useValidator } from '@/hooks/web/useValidator'
import {
  addIssueApi,
  getIssueApi,
  putIssueApi,
  getIssueCategoryOptionsApi
} from '@/api/vadmin/help/issue'
import { useRouter } from 'vue-router'
import { useTagsViewStore } from '@/store/modules/tagsView'

const { required } = useValidator()
const { push, currentRoute } = useRouter()

const { register, methods, elFormRef } = useForm({
  schema: schema
})

const rules = reactive({
  title: [required()],
  content: [required()],
  category_id: [required()]
})

const actionType = ref('')

const initData = async () => {
  const issueId = currentRoute.value.query.id
  if (issueId) {
    actionType.value = 'edit'
    const res = await getIssueApi(Number(issueId))
    if (res) {
      const { setValues } = methods
      setValues(res.data)
    } else {
      // 未获取到数据，跳转到404页面
      push('/404')
    }
  } else {
    actionType.value = 'add'
  }
}

initData()

const getOptions = async () => {
  const { setSchema } = methods
  const res = await getIssueCategoryOptionsApi()
  setSchema([
    {
      field: 'category_id',
      path: 'componentProps.options',
      value: res.data
    }
  ])
}

getOptions()

const editorRef = ref<typeof Editor & EditorExpose>()

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
  autoFocus: false,
  scroll: true,
  readOnly: false,
  uploadImgShowBase64: true,
  placeholder: '请输入内容...'
}

const loading = ref(false)

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
      const tagsViewStore = useTagsViewStore()
      const res = ref({})
      try {
        if (actionType.value === 'add') {
          res.value = await addIssueApi(data)
          if (res.value) {
            // 删除当前标签页，并跳转到列表页
            tagsViewStore.delView(unref(currentRoute))
            push('/help/issue')
          }
        } else if (actionType.value === 'edit') {
          res.value = await putIssueApi(data)
          if (res.value) {
            // 删除当前标签页，并跳转到列表页
            tagsViewStore.delView(unref(currentRoute))
            push('/help/issue')
          }
        }
      } finally {
        loading.value = false
      }
    }
  })
}

defineExpose({
  elFormRef,
  getFormData: methods.getFormData
})
</script>

<template>
  <ContentWrap>
    <Form class="issue-form" :rules="rules" @register="register">
      <template #content="form">
        <Editor
          v-model="form['content']"
          ref="editorRef"
          editorId="issueContent"
          :editorConfig="editorConfig"
        />
      </template>

      <template #active>
        <ElButton type="primary" @click="save">立即保存</ElButton>
      </template>
    </Form>
  </ContentWrap>
</template>

<style lang="less">
.issue-form .el-form-item__content {
  display: block !important;
}
</style>
