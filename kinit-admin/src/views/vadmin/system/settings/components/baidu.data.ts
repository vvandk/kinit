import { FormSchema } from '@/types/form'
import { reactive } from 'vue'

export const schema = reactive<FormSchema[]>([
  {
    field: 'web_baidu',
    label: '百度统计代码',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      rows: 8,
      type: 'textarea',
      style: {
        width: '700px'
      }
    }
  },
  {
    field: 'web_baidu_remard',
    label: '',
    component: 'Text',
    componentProps: {
      modelValue:
        '不包含&lt;script&gt;标签，只需要复制&lt;script&gt;标签内的内容即可，<a href="https://tongji.baidu.com/web5/welcome/login?castk=LTE%3D" target="_blank" style="color: #1890ff">点击注册</a>'
    },
    colProps: {
      span: 24
    }
  },
  {
    field: 'active',
    label: '',
    colProps: {
      span: 24
    }
  }
])
