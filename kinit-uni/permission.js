import { getToken } from '@/common/utils/auth'
import store from '@/store'
import {RouterMount, createRouter} from 'uni-simple-router';

// 登录页面
const loginPage = "/pages/login"

const router = createRouter({
	platform: process.env.VUE_APP_PLATFORM,  
	routes: [...ROUTES]
});

//全局路由前置守卫
router.beforeEach((to, from, next) => {
	if (to.meta.loginAuth) {
		if (getToken()) {
			if (!store.state.auth.isUser) {
				store.dispatch('GetInfo')
			}
			if (to.path === loginPage) {
				uni.reLaunch({ url: "/" })
			}
		} else {
			uni.reLaunch({ url: loginPage })
		}
	}
	next();
});

// 全局路由后置守卫
router.afterEach((to, from) => {
    // console.log('跳转结束')
})

export {
	router,
	RouterMount
}
