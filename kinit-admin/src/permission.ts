import { hasRoute } from './router'
import router from './router'
import type { RouteRecordRaw } from 'vue-router'
import { useTitle } from '@/hooks/web/useTitle'
import { useNProgress } from '@/hooks/web/useNProgress'
import { usePermissionStoreWithOut } from '@/store/modules/permission'
import { usePageLoading } from '@/hooks/web/usePageLoading'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { getRoleMenusApi } from '@/api/login'

const { start, done } = useNProgress()

const { loadStart, loadDone } = usePageLoading()

const whiteList = ['/login', '/docs/privacy', '/docs/agreement'] // 不重定向白名单

router.beforeEach(async (to, from, next) => {
  start()
  loadStart()
  const permissionStore = usePermissionStoreWithOut()
  const authStore = useAuthStoreWithOut()

  if (authStore.getToken) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else if (to.path === '/reset/password') {
      next()
    } else {
      if (!authStore.getIsUser) {
        await authStore.setUserInfo()
      }
      if (permissionStore.getIsAddRouters) {
        if (!hasRoute(to.path)) {
          authStore.logout('认证已过期，请重新登录！')
        }
        next()
        return
      }

      // 开发者可根据实际情况进行修改
      const res = await getRoleMenusApi()
      const routers = res.data || []
      await permissionStore.generateRoutes(routers).catch(() => {})
      permissionStore.getAddRouters.forEach((route) => {
        router.addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
      })
      const redirectPath = from.query.redirect || to.path
      const redirect = decodeURIComponent(redirectPath as string)
      const nextData = to.path === redirect ? { ...to, replace: true } : { path: redirect }
      permissionStore.setIsAddRouters(true)
      next(nextData)
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next(`/login?redirect=${to.path}`) // 否则全部重定向到登录页
    }
  }
})

router.afterEach((to) => {
  useTitle(to?.meta?.title as string)
  done() // 结束Progress
  loadDone()
})
