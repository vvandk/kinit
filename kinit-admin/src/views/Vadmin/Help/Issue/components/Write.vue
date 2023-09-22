<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { reactive, ref } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { useRouter } from 'vue-router'
import { ElButton, ElMessage } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
// import { useTagsViewStore } from '@/store/modules/tagsView'
import {
  addIssueApi,
  getIssueApi,
  putIssueApi,
  getIssueCategoryOptionsApi
} from '@/api/vadmin/help/issue'

defineOptions({
  name: 'HelpIssueForm'
})

const { required } = useValidator()
const { push, currentRoute } = useRouter()

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

const formSchema = reactive<FormSchema[]>([
  {
    field: 'title',
    label: '标题名称',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      }
    },
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'content',
    label: '内容',
    colProps: {
      span: 24
    },
    component: 'Editor',
    componentProps: {
      style: {
        width: '100%'
      },
      editorConfig: editorConfig,
      editorId: 'issueContent'
    },
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'category_id',
    label: '问题类别',
    colProps: {
      span: 24
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      }
    },
    formItemProps: {
      rules: [required()]
    },
    optionApi: async () => {
      const res = await getIssueCategoryOptionsApi()
      return res.data
    }
  },
  {
    field: '',
    label: '',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <ElButton loading={saveLoading.value} type="primary" onClick={submit}>
                立即保存
              </ElButton>
            </>
          )
        }
      }
    }
  }
])

const { formRegister, formMethods } = useForm()
const { getFormData, getElFormExpose, setValues } = formMethods

const actionType = ref('')
const saveLoading = ref(false)

const initData = async () => {
  const issueId = currentRoute.value.query.id
  if (issueId) {
    actionType.value = 'edit'
    const res = await getIssueApi(Number(issueId))
    if (res) {
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

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    saveLoading.value = true
    const formData = await getFormData()

    if (!formData) {
      saveLoading.value = false
      return ElMessage.error('未获取到数据')
    }
    // const tagsViewStore = useTagsViewStore()
    const res = ref()
    try {
      if (actionType.value === 'add') {
        res.value = await addIssueApi(formData)
        if (res.value) {
          // 删除当前标签页，并跳转到列表页
          // tagsViewStore.delView(unref(currentRoute))
          // push('/help/issue')
          elForm?.resetFields()
          ElMessage.success('新增成功')
        }
      } else if (actionType.value === 'edit') {
        res.value = await putIssueApi(formData)
        if (res.value) {
          // 删除当前标签页，并跳转到列表页
          // tagsViewStore.delView(unref(currentRoute))
          // push('/help/issue')
          setValues(res.value.data)
          ElMessage.success('更新成功')
        }
      }
    } finally {
      saveLoading.value = false
    }
  }
}

defineExpose({
  submit
})
</script>

<template>
  <ContentWrap
    ><Form @register="formRegister" :schema="formSchema" labelPosition="top"
  /></ContentWrap>
</template>
