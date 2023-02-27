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
    field: 'telephone',
    label: '手机号',
    width: '150px',
    show: true,
    disabled: true,
    span: 24
  },
  {
    field: 'status',
    label: '登录状态',
    width: '100px',
    show: true,
    span: 24
  },
  {
    field: 'platform',
    label: '登录平台',
    width: '150px',
    show: true,
    span: 24
  },
  {
    field: 'login_method',
    label: '认证方式',
    width: '150px',
    show: true,
    span: 24
  },
  {
    field: 'ip',
    label: '登录地址',
    show: true,
    disabled: true,
    width: '150px',
    span: 24
  },
  {
    field: 'address',
    label: '登录地点',
    show: true,
    span: 24
  },
  {
    field: 'postal_code',
    label: '邮政编码',
    show: false,
    span: 24
  },
  {
    field: 'area_code',
    label: '地区区号',
    show: false,
    span: 24
  },
  {
    field: 'browser',
    label: '浏览器',
    show: true,
    span: 24
  },
  {
    field: 'system',
    label: '操作系统',
    show: true,
    span: 24
  },
  {
    field: 'response',
    label: '响应信息',
    show: false,
    disabled: true,
    span: 24
  },
  {
    field: 'request',
    label: '请求信息',
    show: false,
    disabled: true,
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
    field: 'action',
    label: '操作',
    show: true,
    disabled: false,
    width: '100px',
    span: 24
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'telephone',
    label: '手机号',
    component: 'Input',
    componentProps: {
      clearable: false,
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
    field: 'ip',
    label: '登录地址',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'address',
    label: '登录地点',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'status',
    label: '登录状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '登录成功',
          value: true
        },
        {
          label: '登录失败',
          value: false
        }
      ]
    }
  }
])
