import request from '@/config/axios'
import type { UserLoginType, UserType } from './types'

export const loginApi = (data: UserLoginType): Promise<IResponse> => {
  return request.post({ url: '/auth/login/', data })
}

export const loginOutApi = (): Promise<IResponse> => {
  return request.get({ url: '/user/loginOut' })
}

export const getUserListApi = ({ params }: AxiosConfig) => {
  return request.get<{
    total: number
    list: UserType[]
  }>({ url: '/user/list', params })
}

export const getRoleMenusApi = (): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
  return request.get({ url: '/auth/getMenuList/' })
}
