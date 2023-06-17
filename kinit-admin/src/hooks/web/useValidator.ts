import { useI18n } from '@/hooks/web/useI18n'
import { isEmpty, isNullOrUnDef } from '@/utils/is'

const { t } = useI18n()

type Callback = (error?: string | Error | undefined) => void

interface LengthRange {
  min: number
  max: number
  message: string
}

export const useValidator = () => {
  const required = (message?: string) => {
    return {
      required: true,
      message: message || t('common.required')
    }
  }

  const lengthRange = (val: any, callback: Callback, options: LengthRange) => {
    const { min, max, message } = options
    if (val.length < min || val.length > max) {
      callback(new Error(message))
    } else {
      callback()
    }
  }

  const notSpace = (val: any, callback: Callback, message: string) => {
    // 用户名不能有空格
    if (val.indexOf(' ') !== -1) {
      callback(new Error(message))
    } else {
      callback()
    }
  }

  const notSpecialCharacters = (val: any, callback: Callback, message: string) => {
    // 密码不能是特殊字符
    if (/[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/gi.test(val)) {
      callback(new Error(message))
    } else {
      callback()
    }
  }

  // 两个字符串是否想等
  const isEqual = (val1: string, val2: string, callback: Callback, message: string) => {
    if (val1 === val2) {
      callback()
    } else {
      callback(new Error(message))
    }
  }

  const isEmail = (rule: any, val: any, callback: Callback) => {
    if (isEmpty(val) || isNullOrUnDef(val)) {
      callback()
    }
    // 判断是否为邮箱地址
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
      callback()
    } else {
      callback(new Error('请填写正确的邮箱地址'))
    }
  }

  const isTelephone = (rule: any, val: any, callback: Callback) => {
    if (isEmpty(val) || isNullOrUnDef(val)) {
      callback()
    }
    // 判断是否为正确手机号
    if (/^1[3-9]\d{9}$/.test(val)) {
      callback()
    } else {
      callback(new Error('请填写正确的手机号'))
    }
  }

  const isAmount = (rule: any, val: any, callback: Callback) => {
    if (isEmpty(val) || isNullOrUnDef(val)) {
      callback()
    }
    // 判断是否为正确金额
    if (/^\d+(\.\d{1,2})?$/.test(val)) {
      callback()
    } else {
      callback(new Error('请填写正确的金额格式'))
    }
  }

  return {
    required,
    lengthRange,
    notSpace,
    notSpecialCharacters,
    isEqual,
    isEmail,
    isTelephone,
    isAmount
  }
}
