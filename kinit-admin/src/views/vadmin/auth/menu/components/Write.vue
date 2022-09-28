<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { TableData } from '@/api/table/types'
import { useValidator } from '@/hooks/web/useValidator'
import { getMenuTreeOptionsApi } from '@/api/vadmin/auth/menu'
import { ElButton } from 'element-plus'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<Nullable<TableData>>,
    default: () => null
  }
})

const schema = reactive<FormSchema[]>([
  {
    field: 'parent_id',
    label: '上级菜单',
    colProps: {
      span: 24
    },
    component: 'TreeSelect',
    componentProps: {
      style: {
        width: '100%'
      },
      checkStrictly: true,
      placeholder: '请选择上级菜单'
    }
  },
  {
    field: 'menu_type',
    label: '菜单类型',
    colProps: {
      span: 24
    },
    component: 'Radio',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '目录',
          value: '0'
        },
        {
          label: '菜单',
          value: '1'
        },
        {
          label: '按钮',
          value: '2'
        }
      ]
    },
    value: '0'
  },
  {
    field: 'icon',
    label: '菜单图标',
    component: 'Input',
    colProps: {
      span: 20
    },
    componentProps: {
      placeholder: '支持 Iconify 中的所有图标，请登录网站自行搜索：https://iconify.design/'
    }
  },
  {
    field: 'iconClick',
    label: '',
    colProps: {
      span: 3
    }
  }
])

const rules = reactive({
  title: [required()],
  author: [required()],
  importance: [required()],
  pageviews: [required()],
  display_time: [required()],
  content: [required()]
})

const { register, methods, elFormRef } = useForm({
  schema: schema
})

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    const { setValues } = methods
    setValues(currentRow)
  },
  {
    deep: true,
    immediate: true
  }
)

const getMenuTreeOptions = async () => {
  const res = await getMenuTreeOptionsApi()
  if (res) {
    const { setSchema } = methods
    setSchema([
      {
        field: 'parent_id',
        path: 'componentProps.data',
        value: res.data
      }
    ])
  }
}

getMenuTreeOptions()

defineExpose({
  elFormRef,
  getFormData: methods.getFormData
})
</script>

<template>
  <Form :rules="rules" @register="register">
    <template #iconClick-label>
      <!-- <div>
        <el-button type="primary">跳转</el-button>
      </div> -->
    </template>
    <template #iconClick>
      <div>
        <ElButton type="primary">跳转</ElButton>
      </div>
    </template>
  </Form>
</template>
