import request from '@/config/axios'

export const getTaskListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/tasks', params })
}

export const addTaskListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/vadmin/system/tasks', data })
}

export const delTaskListApi = (dataId: string): Promise<IResponse> => {
  return request.delete({ url: `/vadmin/system/tasks?_id=${dataId}` })
}

export const putTaskListApi = (dataId: string, data: any): Promise<IResponse> => {
  return request.put({ url: `/vadmin/system/tasks?_id=${dataId}`, data })
}

export const getTaskApi = (dataId: string): Promise<IResponse> => {
  return request.get({ url: `/vadmin/system/task?_id=${dataId}` })
}

export const getTaskGroupOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/task/group/options' })
}

export const getTaskRecordListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/vadmin/system/task/records', params })
}

export const runOnceTaskApi = (dataId: string): Promise<IResponse> => {
  return request.post({ url: `/vadmin/system/task?_id=${dataId}` })
}
