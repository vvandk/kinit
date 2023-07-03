import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'job_id',
    label: '任务编号',
    show: true,
    disabled: true,
    width: '240px',
    span: 24
  },
  {
    field: 'name',
    label: '任务名称',
    show: true,
    disabled: true,
    span: 24
  },
  {
    field: 'group',
    label: '任务分组',
    show: true,
    span: 24
  },
  {
    field: 'job_class',
    label: '调用目标',
    show: true,
    span: 24
  },
  {
    field: 'exec_strategy',
    label: '执行策略',
    show: true,
    span: 24
  },
  {
    field: 'expression',
    label: '表达式',
    show: true,
    span: 24
  },
  {
    field: 'start_time',
    label: '开始执行时间',
    show: false,
    width: '200px',
    span: 24
  },
  {
    field: 'end_time',
    label: '执行完成时间',
    width: '200px',
    show: true,
    span: 24
  },
  {
    field: 'process_time',
    label: '耗时(秒)',
    width: '110px',
    show: true,
    span: 24
  },
  {
    field: 'retval',
    label: '任务返回值',
    show: true,
    span: 24
  },
  {
    field: 'exception',
    label: '异常信息',
    show: false,
    span: 24
  },
  {
    field: 'traceback',
    label: '堆栈跟踪',
    show: false,
    width: '100px',
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
    field: 'job_id',
    label: '任务编号',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '240px'
      }
    }
  },
  {
    field: 'name',
    label: '任务名称',
    component: 'Input',
    componentProps: {
      clearable: true
    }
  }
])
