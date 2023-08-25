import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    show: true,
    disabled: false,
    width: '120px',
    span: 24
  },
  {
    field: 'image_url',
    label: '图片',
    show: true,
    disabled: true,
    minWidth: '90px',
    span: 24
  },
  {
    field: 'remark',
    label: '备注',
    show: false,
    disabled: false,
    span: 24
  },
  {
    field: 'update_datetime',
    label: '更新时间',
    show: false,
    width: '180px',
    span: 24
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    width: '180px',
    show: true,
    span: 24
  },
  {
    field: 'create_user.name',
    label: '创建人',
    show: false,
    span: 24
  },
  {
    field: 'action',
    label: '操作',
    show: true,
    disabled: false,
    width: '260px',
    fixed: 'right',
    span: 24
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'filename',
    label: '文件名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  }
])

export const schema = reactive<FormSchema[]>([
  {
    field: 'upload_method',
    label: '上传方式',
    colProps: {
      span: 24
    },
    component: 'Radio',
    componentProps: {
      options: [
        {
          label: '同时上传',
          value: '1'
        },
        {
          label: '按顺序上传',
          value: '2'
        }
      ]
    },
    value: '1'
  },
  {
    field: 'images',
    label: '',
    colProps: {
      span: 24
    }
  }
])
