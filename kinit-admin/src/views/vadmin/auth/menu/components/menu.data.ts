import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'title',
    label: '菜单名称',
    width: '200px'
  },
  {
    field: 'icon',
    label: '图标',
    width: '120px'
  },
  {
    field: 'order',
    label: '排序',
    width: '120px'
  },
  {
    field: 'menu_type',
    label: '菜单类型',
    width: '120px'
  },
  {
    field: 'perms',
    label: '权限标识',
    width: '150px'
  },
  {
    field: 'path',
    label: '路由地址'
  },
  {
    field: 'component',
    label: '组件路径'
  },
  {
    field: 'hidden',
    label: '显示状态',
    width: '120px'
  },
  {
    field: 'disabled',
    label: '菜单状态',
    width: '120px'
  },
  {
    field: 'action',
    width: '200px',
    label: '操作'
  }
])

export const schema = reactive<FormSchema[]>([
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
    colProps: {
      span: 24
    },
    ifshow: (values) => values.menu_type !== '2'
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
    },
    ifshow: (values) => values.menu_type !== '2'
  },
  {
    field: 'component',
    label: '组件路径',
    component: 'Input',
    colProps: {
      span: 12
    },
    ifshow: (values) => values.menu_type !== '2'
  },
  {
    field: 'redirect',
    label: '重定向',
    component: 'Input',
    colProps: {
      span: 12
    },
    ifshow: (values) => values.menu_type !== '2'
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
          value: false
        },
        {
          label: '隐藏',
          value: true
        }
      ]
    },
    value: false,
    ifshow: (values) => values.menu_type !== '2'
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
    value: false,
    ifshow: (values) => values.menu_type !== '2'
  },
  {
    field: 'perms',
    label: '权限标识',
    component: 'Input',
    colProps: {
      span: 12
    },
    ifshow: (values) => values.menu_type !== '0'
  }
])
