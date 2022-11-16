import type { CSSProperties } from 'vue'
import { ColProps, ComponentProps, ComponentName } from '@/types/components'
import { FormValueType, FormValueType } from '@/types/form'
import type { AxiosPromise } from 'axios'

export type FormSetPropsType = {
  field: string
  path: string
  value: any
}

export type FormValueType = string | number | string[] | number[] | boolean | undefined | null

export type FormItemProps = {
  labelWidth?: string | number
  required?: boolean
  rules?: Recordable
  error?: string
  showMessage?: boolean
  inlineMessage?: boolean
  style?: CSSProperties
}

export type FormSchema = {
  // 唯一值
  field: string
  // 标题
  label?: string
  // 提示
  labelMessage?: string
  // col组件属性
  colProps?: ColProps
  // 表单组件属性，slots对应的是表单组件的插槽，规则：${field}-xxx，具体可以查看element-plus文档
  componentProps?: { slots?: Recordable } & ComponentProps
  // formItem组件属性
  formItemProps?: FormItemProps
  // 渲染的组件
  component?: ComponentName
  // 初始值
  value?: FormValueType
  // 是否隐藏，隐藏后就不会在formModel中显示了，不会获取到该字段的值
  hidden?: boolean
  // 是否显示，隐藏后还会在formModel中显示，可以获取到该字段的值
  ifshow?: (values: Recordable) => boolean
  // 远程加载下拉项
  api?: <T = any>() => AxiosPromise<T>
}
