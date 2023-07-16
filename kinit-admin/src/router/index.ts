import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'
import { Layout } from '@/utils/routerHelper'
import { useI18n } from '@/hooks/web/useI18n'

const { t } = useI18n()

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Root',
    meta: {
      hidden: true,
      title: '首页',
      noTagsView: true
    },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home/Home.vue'),
        meta: {
          affix: false,
          alwaysShow: true,
          breadcrumb: true,
          canTo: true,
          hidden: true,
          icon: null,
          noCache: true,
          noTagsView: false,
          title: '个人主页'
        }
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/Login/Login.vue'),
    name: 'Login',
    meta: {
      hidden: true,
      title: t('router.login'),
      noTagsView: true
    }
  },
  {
    path: '/reset/password',
    component: () => import('@/views/Reset/Reset.vue'),
    name: 'ResetPassword',
    meta: {
      hidden: true,
      title: '重置密码',
      noTagsView: true
    }
  },
  {
    path: '/404',
    component: () => import('@/views/Error/404.vue'),
    name: 'NoFind',
    meta: {
      hidden: true,
      title: '404',
      noTagsView: true
    }
  },
  {
    path: '/docs',
    name: 'Docs',
    meta: {
      hidden: true,
      title: '在线文档',
      noTagsView: true
    },
    children: [
      {
        path: 'privacy',
        name: 'Privacy',
        component: () => import('@/views/vadmin/system/docs/privacy.vue'),
        meta: {
          hidden: true,
          title: '隐私政策',
          noTagsView: true
        }
      },
      {
        path: 'agreement',
        name: 'Agreement',
        component: () => import('@/views/vadmin/system/docs/agreement.vue'),
        meta: {
          hidden: true,
          title: '用户协议',
          noTagsView: true
        }
      }
    ]
  }
]

export const asyncRouterMap: AppRouteRecordRaw[] = []

const router = createRouter({
  history: createWebHistory(), // HTML5 模式，https://router.vuejs.org/zh/guide/essentials/history-mode.html#hash-%E6%A8%A1%E5%BC%8F
  // history: createWebHashHistory(), // Hash 模式，https://router.vuejs.org/zh/guide/essentials/history-mode.html#hash-%E6%A8%A1%E5%BC%8F
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const resetRouter = (): void => {
  const resetWhiteNameList = [
    'Home',
    'Login',
    'NoFind',
    'Root',
    'ResetPassword',
    'Docs',
    'Privacy',
    'Agreement'
  ]
  router.getRoutes().forEach((route) => {
    // 切记 name 不能重复
    const { name } = route
    if (name && !resetWhiteNameList.includes(name as string)) {
      router.hasRoute(name) && router.removeRoute(name)
    }
  })
}

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export default router
