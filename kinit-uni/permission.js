import { getToken } from '@/common/utils/auth'
import store from '@/store'
import { RouterMount, createRouter } from 'uni-simple-router';

// 登录页面
const loginPage = "/pages/login/login"

const router = createRouter({
	platform: process.env.VUE_APP_PLATFORM,  
	routes: [...ROUTES]
});

//全局路由前置守卫
router.beforeEach((to, from, next) => {
	if (to.meta.loginAuth) {
		// 如果跳转的路由需要登录权限，则验证该权限
		if (getToken()) {
			if (!store.state.auth.isUser) {
				store.dispatch('auth/GetInfo')
			}
			if (to.path === loginPage) {
				next({
				  path: `/pages/index`,
				  NAVTYPE: 'replaceAll'
				})
			}
			next();
		} else {
			next({
			  path: loginPage,
			  NAVTYPE: 'replaceAll'
			})
		}
	} else if (to.path === loginPage && getToken()) {
		// 如果跳转路由为登录页面并且存在token，则跳转到首页
		next({
      path: `/pages/index`,
      NAVTYPE: 'replaceAll'
    })
	} else {
		// 不需要权限，且不是登录页面则不进行验证
		next();
	}
});

// 全局路由后置守卫
router.afterEach((to, from) => {
    // console.log('跳转结束')
})

export {
	router,
	RouterMount
}
