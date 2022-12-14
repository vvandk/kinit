import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'telephone',
    label: '手机号',
    show: true,
    disabled: true,
    width: '130px',
    span: 24
  },
  {
    field: 'request_method',
    label: '请求方法',
    show: true,
    disabled: true,
    width: '100px',
    span: 24
  },
  {
    field: 'request_ip',
    label: '登陆地址',
    width: '130px',
    show: true,
    disabled: true,
    span: 24
  },
  {
    field: 'tags',
    label: '标签',
    width: '130px',
    show: true,
    span: 24
  },
  {
    field: 'summary',
    label: '操作内容',
    show: true,
    span: 24
  },
  {
    field: 'description',
    label: '描述',
    show: false,
    span: 24
  },
  {
    field: 'status_code',
    label: '操作状态',
    show: true,
    width: '100px',
    span: 24
  },
  {
    field: 'name',
    label: '接口函数',
    show: false,
    width: '150px',
    span: 24
  },
  {
    field: 'api_path',
    label: '接口地址',
    show: false,
    span: 24
  },
  {
    field: 'params',
    label: '请求参数',
    show: false,
    span: 24
  },
  {
    field: 'browser',
    label: '浏览器',
    show: true,
    width: '150px',
    span: 24
  },
  {
    field: 'system',
    label: '系统',
    show: true,
    width: '150px',
    span: 24
  },
  {
    field: 'process_time',
    label: '总耗时',
    show: true,
    span: 24
  },
  {
    field: 'create_datetime',
    label: '操作时间',
    show: true,
    span: 24
  },
  {
    field: 'action',
    width: '100px',
    label: '操作',
    show: true,
    disabled: true,
    span: 24
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'telephone',
    label: '手机号',
    component: 'Input',
    componentProps: {
      clearable: false
    }
  },
  {
    field: 'request_method',
    label: '请求方法',
    component: 'Input',
    componentProps: {
      clearable: false
    }
  },
  {
    field: 'summary',
    label: '操作内容',
    component: 'Input',
    componentProps: {
      clearable: false
    }
  }
])
