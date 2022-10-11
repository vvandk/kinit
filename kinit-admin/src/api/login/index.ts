import request from '@/config/axios'
import type { UserLoginType } from './types'

export const loginApi = (data: UserLoginType): Promise<IResponse> => {
  return request.post({ url: '/auth/login/', data })
}

export const getRoleMenusApi = (): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
  return request.get({ url: '/auth/getMenuList/' })
}
