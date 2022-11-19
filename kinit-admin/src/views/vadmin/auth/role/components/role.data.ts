import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '角色编号',
    show: true,
    disabled: true
  },
  {
    field: 'name',
    label: '角色名称',
    show: true,
    disabled: true
  },
  {
    field: 'role_key',
    label: '权限字符',
    show: true
  },
  {
    field: 'order',
    label: '显示顺序',
    show: true
  },
  {
    field: 'disabled',
    label: '角色状态',
    show: true
  },
  {
    field: 'is_admin',
    label: '最高权限',
    show: true
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true
  },
  {
    field: 'action',
    width: '150px',
    label: '操作',
    show: true
  }
])

export const schema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '角色名称',
    colProps: {
      span: 12
    },
    component: 'Input'
  },
  {
    field: 'role_key',
    label: '权限字符',
    colProps: {
      span: 12
    },
    component: 'Input'
  },
  {
    field: 'disabled',
    label: '角色状态',
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
          label: '禁用',
          value: true
        }
      ]
    },
    value: false
  },
  {
    field: 'is_admin',
    label: '最高权限',
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
          label: '使用',
          value: true
        },
        {
          label: '不使用',
          value: false
        }
      ]
    },
    value: false
  },
  {
    field: 'order',
    label: '显示排序',
    colProps: {
      span: 12
    },
    component: 'InputNumber',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'desc',
    label: '描述',
    colProps: {
      span: 12
    },
    component: 'Input'
  },
  {
    field: 'menu_ids',
    label: '菜单权限',
    colProps: {
      span: 24
    }
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '角色名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'role_key',
    label: '权限字符',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'disabled',
    label: '状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
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
    }
  }
])
