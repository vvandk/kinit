<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { TableData } from '@/api/table/types'
import { useValidator } from '@/hooks/web/useValidator'
import { getMenuTreeOptionsApi } from '@/api/vadmin/auth/menu'
import { ElButton, ElInput } from 'element-plus'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<Nullable<TableData>>,
    default: () => null
  }
})

const handleRadioChange = (item: string) => {
  console.log(item)
}

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
      ],
      onChange: handleRadioChange
    },
    value: '0'
  },
  {
    field: 'icon',
    label: '菜单图标',
    colProps: {
      span: 24
    }
  },
  {
    field: 'title',
    label: '菜单名称',
    component: 'Input',
    colProps: {
      span: 12
    }
  },
  {
    field: 'order',
    label: '显示排序',
    component: 'InputNumber',
    colProps: {
      span: 12
    }
  },
  {
    field: 'path',
    label: '路由地址',
    component: 'Input',
    colProps: {
      span: 12
    }
  },
  {
    field: 'component',
    label: '组件路径',
    component: 'Input',
    colProps: {
      span: 12
    }
  },
  {
    field: 'hidden',
    label: '显示状态',
    colProps: {
      span: 12
    },
    component: 'Radio',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '显示',
          value: true
        },
        {
          label: '隐藏',
          value: false
        }
      ]
    },
    value: true
  },
  {
    field: 'disabled',
    label: '菜单状态',
    colProps: {
      span: 12
    },
    component: 'Radio',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '正常',
          value: false
        },
        {
          label: '停用',
          value: true
        }
      ]
    },
    value: false
  },
  {
    field: 'perms',
    label: '权限标识',
    component: 'Input',
    colProps: {
      span: 24
    },
    hidden: true
  }
])

const rules = reactive({
  title: [required()],
  disabled: [required()],
  hidden: [required()],
  path: [required()],
  order: [required()]
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

const toIconify = () => {
  window.open('https://iconify.design/')
}

defineExpose({
  elFormRef,
  getFormData: methods.getFormData
})
</script>

<template>
  <Form :rules="rules" @register="register">
    <template #icon="form">
      <div style="display: flex; justify-content: space-between">
        <ElInput
          v-model="form['icon']"
          placeholder="支持 Iconify 中的所有图标，请登录网站自行搜索：https://iconify.design/"
          style="width: 500px"
        />
        <div style="margin-left: 10px">
          <ElButton type="primary" @click="toIconify">跳转</ElButton>
        </div>
      </div>
    </template>
  </Form>
</template>
