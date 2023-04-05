import { FormSchema } from '@/types/form'
import { reactive } from 'vue'

export const schema = reactive<FormSchema[]>([
  {
    field: 'email_access',
    label: '邮箱账号',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'email_password',
    label: '邮箱密码',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'email_server',
    label: '邮箱服务器',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'email_port',
    label: '服务器端口',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '500px'
      }
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
