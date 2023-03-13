import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    show: true,
    disabled: true,
    span: 24
  },
  {
    field: 'name',
    label: '类别名称',
    show: true,
    disabled: true,
    span: 24
  },
  {
    field: 'platform',
    label: '展示平台',
    show: true,
    span: 24
  },
  {
    field: 'is_active',
    label: '是否可见',
    show: true,
    span: 24
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true,
    span: 24,
    sortable: true
  },
  {
    field: 'user.name',
    label: '创建人',
    show: true,
    span: 24
  },
  {
    field: 'action',
    label: '操作',
    show: true,
    disabled: false,
    span: 24
  }
])

export const schema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '类别名称',
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
    field: 'platform',
    label: '展示平台',
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
    field: 'is_active',
    label: '是否可见',
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
          label: '可见',
          value: true
        },
        {
          label: '不可见',
          value: false
        }
      ]
    },
    value: true
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '类别名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'platform',
    label: '登录平台',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: []
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
