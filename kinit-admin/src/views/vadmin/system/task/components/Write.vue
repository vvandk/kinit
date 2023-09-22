<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { useDictStore } from '@/store/modules/dict'
import { getTaskGroupOptionsApi } from '@/api/vadmin/system/task'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
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
    },
    formItemProps: {
      rules: [required()]
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
    },
    optionApi: async () => {
      const res = await getTaskGroupOptionsApi()
      return res.data
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
    },
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'exec_strategy',
    label: '执行策略',
    colProps: {
      span: 24
    },
    component: 'RadioGroup',
    componentProps: {
      style: {
        width: '100%'
      }
    },
    value: 'interval',
    formItemProps: {
      rules: [required()]
    },
    optionApi: async () => {
      const dictStore = useDictStore()
      const dictOptions = await dictStore.getDictObj(['vadmin_system_task_exec_strategy'])
      return dictOptions.vadmin_system_task_exec_strategy
    }
    // formItemProps: {
    //   slots: {
    //     default: (data) => {
    //       return (
    //         <>
    //           <ElRadioGroup v-model={data['exec_strategy']} onChange={handleChange(form)}></>
    //     <ElRadio v-for="(item, $index) in execStrategyOptions" :key="" :label="item.value">{{
    //       item.label
    //     }}</ElRadio>
    //     {}
    //   </ElRadioGroup>
    //         </>
    //       )
    //     }
    //   }
    // }
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
    ifshow: (values) => values.exec_strategy === 'interval',
    formItemProps: {
      rules: [required()]
    }
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
    ifshow: (values) => values.exec_strategy === 'cron',
    formItemProps: {
      rules: [required()]
    }
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
    ifshow: (values) => values.exec_strategy === 'date',
    formItemProps: {
      rules: [required()]
    }
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
    component: 'RadioGroup',
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
  }
])

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await getFormData()
    return formData
  }
}

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    setValues(currentRow)
  },
  {
    deep: true,
    immediate: true
  }
)

defineExpose({
  submit
})
</script>

<template>
  <Form @register="formRegister" :schema="formSchema" />
</template>
