import router from './router'
import { useAppStoreWithOut } from '@/store/modules/app'
import { useCache } from '@/hooks/web/useCache'
import type { RouteRecordRaw } from 'vue-router'
import { useTitle } from '@/hooks/web/useTitle'
import { useNProgress } from '@/hooks/web/useNProgress'
import { useRouterStoreWithOut } from '@/store/modules/router'
import { usePageLoading } from '@/hooks/web/usePageLoading'
import { getRoleMenusApi } from '@/api/login'
import { useAuthStoreWithOut } from '@/store/modules/auth'

const Routertore = useRouterStoreWithOut()

const appStore = useAppStoreWithOut()
const authStore = useAuthStoreWithOut()

const { wsCache } = useCache()

const { start, done } = useNProgress()

const { loadStart, loadDone } = usePageLoading()

const whiteList = ['/login', '/docs/privacy', '/docs/agreement'] // 不重定向白名单

router.beforeEach(async (to, from, next) => {
  start()
  loadStart()
  if (wsCache.get(appStore.getToken)) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else if (to.path === '/reset/password') {
      next()
    } else {
      if (!authStore.getIsUser) {
        await authStore.setUserInfo()
      }
      if (Routertore.getIsAddRouters) {
        next()
        return
      }

      // 开发者可根据实际情况进行修改
      const res = await getRoleMenusApi()
      const { wsCache } = useCache()
      const routers = res.data || []
      wsCache.set('roleRouters', routers)
      await Routertore.generateRoutes(routers).catch(() => {})
      Routertore.getAddRouters.forEach((route) => {
        router.addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
      })
      const redirectPath = from.query.redirect || to.path
      const redirect = decodeURIComponent(redirectPath as string)
      const nextData = to.path === redirect ? { ...to, replace: true } : { path: redirect }
      Routertore.setIsAddRouters(true)
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
