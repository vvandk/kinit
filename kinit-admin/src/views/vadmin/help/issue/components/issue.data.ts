import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    show: true,
    disabled: true,
    width: '120px',
    span: 24
  },
  {
    field: 'category.name',
    label: '类别名称',
    width: '200px',
    show: true,
    disabled: true,
    span: 24
  },
  {
    field: 'title',
    label: '标题',
    show: true,
    span: 24
  },
  {
    field: 'view_number',
    label: '查看次数',
    show: true,
    width: '100px',
    span: 24
  },
  {
    field: 'is_active',
    label: '是否可见',
    show: true,
    width: '100px',
    span: 24
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true,
    width: '200px',
    span: 24,
    sortable: true
  },
  {
    field: 'user.name',
    label: '创建人',
    show: true,
    width: '100px',
    span: 24
  },
  {
    field: 'action',
    label: '操作',
    show: true,
    disabled: false,
    width: '100px',
    span: 24
  }
])

export const schema = reactive<FormSchema[]>([
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
    }
  },
  {
    field: 'content',
    label: '解答内容',
    colProps: {
      span: 24
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
    }
  },
  {
    field: 'active',
    label: ' ',
    colProps: {
      span: 24
    }
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'title',
    label: '标题',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    },
    formItemProps: {
      labelWidth: '47px'
    }
  },
  {
    field: 'category_id',
    label: '类别名称',
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'is_active',
    label: '是否可见',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '可见',
          value: true
        },
        {
          label: '不可见',
          value: false
        }
      ]
    }
  }
])
