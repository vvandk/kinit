import { reactive } from 'vue'

export const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '用户编号'
  },
  {
    field: 'name',
    label: '姓名'
  },
  {
    field: 'nickname',
    label: '昵称'
  },
  {
    field: 'telephone',
    label: '手机号'
  },
  {
    field: 'gender',
    label: '性别'
  },
  {
    field: 'is_active',
    label: '是否可用'
  },
  {
    field: 'last_login',
    label: '最近一次登录时间'
  },
  {
    field: 'create_datetime',
    label: '创建时间'
  },
  {
    field: 'action',
    width: '260px',
    label: '操作'
  }
])

export const schema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '用户名称',
    colProps: {
      span: 12
    },
    component: 'Input'
  },
  {
    field: 'telephone',
    label: '手机号码',
    colProps: {
      span: 12
    },
    component: 'Input'
  },
  {
    field: 'nickname',
    label: '用户昵称',
    colProps: {
      span: 12
    },
    component: 'Input'
  },
  {
    field: 'gender',
    label: '性别',
    colProps: {
      span: 12
    },
    component: 'Radio',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '男',
          value: '0'
        },
        {
          label: '女',
          value: '1'
        }
      ]
    },
    value: '0'
  },
  {
    field: 'is_active',
    label: '状态',
    colProps: {
      span: 12
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
    field: 'role_ids',
    label: '角色',
    colProps: {
      span: 24
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      optionsAlias: {
        labelField: 'name',
        valueField: 'id'
      },
      multiple: true,
      collapseTags: true
    },
    value: []
  }
])
