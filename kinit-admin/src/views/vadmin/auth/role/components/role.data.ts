import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '角色编号'
  },
  {
    field: 'name',
    label: '角色名称'
  },
  {
    field: 'role_key',
    label: '权限字符'
  },
  {
    field: 'order',
    label: '显示顺序'
  },
  {
    field: 'disabled',
    label: '角色状态'
  },
  {
    field: 'is_admin',
    label: '最高权限'
  },
  {
    field: 'create_datetime',
    label: '创建时间'
  },
  {
    field: 'action',
    width: '260px',
    label: '操作'
  }
])

export const schema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '角色名称',
    colProps: {
      span: 24
    },
    component: 'Input'
  },
  {
    field: 'role_key',
    label: '权限字符',
    colProps: {
      span: 24
    },
    component: 'Input'
  },
  {
    field: 'order',
    label: '显示排序',
    colProps: {
      span: 24
    },
    component: 'InputNumber'
  },
  {
    field: 'disabled',
    label: '角色状态',
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
      span: 24
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
    field: 'desc',
    label: '描述',
    colProps: {
      span: 24
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
