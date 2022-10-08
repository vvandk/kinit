import { defineStore } from 'pinia'
import { store } from '../index'
import { getDictTypeDetailsApi } from '@/api/vadmin/system/dict'

export interface DictState {
  dictObj: Recordable
}

export const useDictStore = defineStore({
  id: 'dict',
  state: (): DictState => ({
    dictObj: {}
  }),
  persist: {
    // 开启持久化存储
    enabled: true
  },
  getters: {},
  actions: {
    async getDictObj(dictTypes: string[]) {
      const result: Recordable = {}
      const addList: string[] = []
      for (const item of dictTypes) {
        if (item in this.dictObj) {
          result[item] = this.dictObj[item]
        } else {
          result[item] = []
          addList.push(item)
        }
      }
      if (addList.length > 0) {
        const res = await getDictTypeDetailsApi(addList)
        if (res) {
          for (const item of addList) {
            result[item] = res.data[item]
            this.dictObj[item] = res.data[item]
          }
        }
      }
      return result
    }
  }
})

export const useDictStoreWithOut = () => {
  return useDictStore(store)
}
