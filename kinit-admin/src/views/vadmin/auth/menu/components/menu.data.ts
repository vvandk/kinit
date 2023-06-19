import { reactive } from 'vue'
import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'

export const columns = reactive<TableColumn[]>([
  {
    field: 'title',
    label: '菜单名称',
    width: '200px',
    disabled: true,
    show: true
  },
  {
    field: 'icon',
    label: '图标',
    width: '120px',
    show: false
  },
  {
    field: 'order',
    label: '排序',
    width: '120px',
    show: true
  },
  {
    field: 'menu_type',
    label: '菜单类型',
    width: '120px',
    show: true
  },
  {
    field: 'perms',
    label: '权限标识',
    width: '150px',
    show: true
  },
  {
    field: 'path',
    label: '路由地址',
    show: true
  },
  {
    field: 'component',
    label: '组件路径',
    show: true
  },
  {
    field: 'noCache',
    label: '页面缓存',
    width: '120px',
    show: true
  },
  {
    field: 'hidden',
    label: '显示状态',
    width: '120px',
    show: true
  },
  {
    field: 'disabled',
    label: '菜单状态',
    width: '120px',
    show: true
  },
  {
    field: 'action',
    width: '200px',
    label: '操作',
    show: true
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
      placeholder: '请选择上级菜单',
      nodeKey: 'value',
      defaultExpandAll: true
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
    component: 'Input',
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
    },
    componentProps: {
      style: {
        width: '100%'
      }
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
    ifshow: (values) => values.menu_type === '2'
  },
  {
    field: 'noCache',
    label: '页面缓存',
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
          label: '缓存',
          value: false
        },
        {
          label: '不缓存',
          value: true
        }
      ]
    },
    value: false,
    ifshow: (values) => values.menu_type === '1',
    labelMessage: '开启页面缓存,需要组件名称必须与xx.vue页面的name一致'
  }
])
