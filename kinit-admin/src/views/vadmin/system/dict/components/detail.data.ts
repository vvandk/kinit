import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { ElTag } from 'element-plus'
import { h, reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '字典编号',
    show: true,
    disabled: true
  },
  {
    field: 'label',
    label: '字典标签',
    show: true,
    disabled: true
  },
  {
    field: 'value',
    label: '字典键值',
    show: true
  },
  {
    field: 'order',
    label: '字典排序',
    show: true
  },
  {
    field: 'disabled',
    label: '是否禁用',
    formatter: (_: Recordable, __: TableColumn, cellValue: number) => {
      return h(
        ElTag,
        {
          type: cellValue ? 'danger' : ''
        },
        () => (cellValue ? '禁用' : '启用')
      )
    },
    show: true
  },
  {
    field: 'remark',
    label: '备注',
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
    field: 'label',
    label: '字典标签',
    colProps: {
      span: 24
    },
    component: 'Input'
  },
  {
    field: 'value',
    label: '字典键值',
    colProps: {
      span: 24
    },
    component: 'Input'
  },
  {
    field: 'order',
    label: '排序',
    colProps: {
      span: 24
    },
    component: 'InputNumber',
    componentProps: {
      style: {
        width: '50%'
      }
    }
  },
  {
    field: 'is_default',
    label: '是否默认',
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
          label: '是',
          value: true
        },
        {
          label: '否',
          value: false
        }
      ]
    },
    value: false
  },
  {
    field: 'disabled',
    label: '是否禁用',
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
          label: '启用',
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
    field: 'remark',
    label: '备注',
    colProps: {
      span: 24
    },
    component: 'Input'
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'label',
    label: '字典标签',
    component: 'Input',
    componentProps: {
      clearable: false
    }
  },
  {
    field: 'dict_type_id',
    label: '字典类型',
    component: 'Select',
    componentProps: {
      optionsAlias: {
        labelField: 'dict_name',
        valueField: 'id'
      },
      clearable: false
    }
  }
])
