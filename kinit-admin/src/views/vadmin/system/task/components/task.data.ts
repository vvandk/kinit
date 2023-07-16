import { FormSchema } from '@/types/form'
import { TableColumn } from '@/types/table'
import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: '_id',
    label: '任务编号',
    show: true,
    disabled: true,
    width: '240px',
    span: 24
  },
  {
    field: 'name',
    label: '任务名称',
    width: '200px',
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
    component: 'Radio',
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
    field: 'expression',
    label: '表达式',
    show: true,
    span: 24
  },
  {
    field: 'is_active',
    label: '任务状态',
    show: true,
    width: '100px',
    span: 24
  },
  {
    field: 'last_run_datetime',
    label: '最近一次执行时间',
    show: true,
    width: '200px',
    span: 24
  },
  {
    field: 'remark',
    label: '任务备注',
    show: true,
    span: 24
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true,
    width: '200px',
    span: 24
  },
  {
    field: 'action',
    label: '操作',
    show: true,
    disabled: false,
    width: '240px',
    span: 24
  }
])

export const schema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '任务名称',
    component: 'Input',
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
    field: 'group',
    label: '任务分组',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      allowCreate: true,
      filterable: true,
      defaultFirstOption: true,
      placeholder: '请选择任务分组，支持直接输入添加'
    }
  },
  {
    field: 'job_class',
    label: '调用目标',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder:
        '调用示例：test.main.Test("kinit", 1314, True)；参数仅支持字符串，整数，浮点数，布尔类型。'
    }
  },
  {
    field: 'exec_strategy',
    label: '执行策略',
    colProps: {
      span: 24
    },
    component: 'Radio',
    componentProps: {
      style: {
        width: '100%'
      }
    },
    value: 'interval'
  },
  {
    field: 'expression',
    label: '表达式',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder:
        'interval 表达式，五位，分别为：秒 分 时 天 周，例如：10 * * * * 表示每隔 10 秒执行一次任务。'
    },
    ifshow: (values) => values.exec_strategy === 'interval'
  },
  {
    field: 'expression',
    label: '表达式',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: 'cron 表达式，六位或七位，分别表示秒、分钟、小时、天、月、星期几、年(可选)'
    },
    ifshow: (values) => values.exec_strategy === 'cron'
  },
  {
    field: 'expression',
    label: '执行时间',
    component: 'DatePicker',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'datetime',
      format: 'YYYY-MM-DD HH:mm:ss',
      valueFormat: 'YYYY-MM-DD HH:mm:ss'
    },
    ifshow: (values) => values.exec_strategy === 'date'
  },
  {
    field: 'start_date',
    label: '开始时间',
    colProps: {
      span: 12
    },
    component: 'DatePicker',
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'datetime',
      format: 'YYYY-MM-DD HH:mm:ss',
      valueFormat: 'YYYY-MM-DD HH:mm:ss'
    },
    ifshow: (values) => values.exec_strategy !== 'date'
  },
  {
    field: 'end_date',
    label: '结束时间',
    colProps: {
      span: 12
    },
    component: 'DatePicker',
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'datetime',
      format: 'YYYY-MM-DD HH:mm:ss',
      valueFormat: 'YYYY-MM-DD HH:mm:ss'
    },
    ifshow: (values) => values.exec_strategy !== 'date'
  },
  {
    field: 'is_active',
    label: '任务状态',
    colProps: {
      span: 8
    },
    component: 'Radio',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '正常',
          value: true
        },
        {
          label: '停用',
          value: false
        }
      ]
    },
    value: true
  },
  {
    field: '',
    label: '',
    colProps: {
      span: 16
    },
    component: 'Text',
    value:
      '创建或更新任务完成后，如果任务状态与设置的不符，请尝试刷新数据或查看调度日志，任务状态可能会有延迟(几秒)。'
  },
  {
    field: 'remark',
    label: '备注说明',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      maxlength: '1000',
      showWordLimit: true,
      type: 'textarea',
      rows: '3'
    }
  },
  {
    field: 'active',
    label: ' ',
    colProps: {
      span: 24
    }
  }
])

export const searchSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '任务名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: '_id',
    label: '任务编号',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'group',
    label: '任务分组',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: []
    }
  }
])
