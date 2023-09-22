import type { App, Directive, DirectiveBinding } from 'vue'
import { useI18n } from '@/hooks/web/useI18n'
import { intersection } from 'lodash-es'
import { isArray } from '@/utils/is'
import { useAuthStoreWithOut } from '@/store/modules/auth'

const { t } = useI18n()
const authStore = useAuthStoreWithOut()

// 全部权限
const all_permission = ['*.*.*']
const hasPermission = (value: string | string[]): boolean => {
  const permissions = authStore.getPermissions
  if (!value) {
    throw new Error(t('permission.hasPermission'))
  }

  if (all_permission[0] === permissions[0]) {
    return true
  }

  if (!isArray(value)) {
    return permissions?.includes(value as string)
  }

  return (intersection(value, permissions) as string[]).length > 0
}
function hasPermi(el: Element, binding: DirectiveBinding) {
  const value = binding.value

  const flag = hasPermission(value)
  if (!flag) {
    el.parentNode?.removeChild(el)
  }
}
const mounted = (el: Element, binding: DirectiveBinding<any>) => {
  hasPermi(el, binding)
}

const permiDirective: Directive = {
  mounted
}

export const setupPermissionDirective = (app: App<Element>) => {
  app.directive('hasPermi', permiDirective)
}

export default permiDirective
