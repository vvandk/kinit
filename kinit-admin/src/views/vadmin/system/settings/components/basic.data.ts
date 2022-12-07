import { FormSchema } from '@/types/form'
import { reactive } from 'vue'

export const schema = reactive<FormSchema[]>([
  {
    field: 'web_title',
    label: '系统标题',
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
    field: 'web_logo',
    label: '系统 LOGO',
    colProps: {
      span: 24
    }
  },
  {
    field: 'web_desc',
    label: '系统描述',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      rows: 4,
      type: 'textarea',
      style: {
        width: '500px'
      }
    }
  },
  {
    field: 'web_ico',
    label: 'ICO 图标',
    colProps: {
      span: 24
    }
  },
  {
    field: 'web_ico_local_path',
    label: 'ICO 图标服务器文件地址',
    colProps: {
      span: 24
    },
    ifshow: () => {
      return false
    }
  },
  {
    field: 'web_icp_number',
    label: '备案号',
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
    field: 'web_copyright',
    label: '版权信息',
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
