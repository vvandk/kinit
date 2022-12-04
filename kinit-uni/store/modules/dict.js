import { getDictTypeDetailsApi } from '@/common/request/api/vadmin/system/dict.js'

const dict = {
  state: {
    dictObj: {}, // 字典元素
  },

  mutations: {
		SET_DICT_OBJ: (state, dictObj) => {
		  state.dictObj = dictObj
		}
  },

  actions: {
    // 初始化系统配置
    getDicts({ commit, getters }, dictTypes) {
			return new Promise((resolve, reject) => {
				const result = {}
				const addList = []
				const dictObj = JSON.parse(JSON.stringify(getters.dictObj))
				for (const item of dictTypes) {
					if (item in dictObj) {
						result[item] = dictObj[item]
					} else {
						result[item] = []
						addList.push(item)
					}
				}
				if (addList.length > 0) {
					getDictTypeDetailsApi(addList).then(res => {
						for (const item of addList) {
							result[item] = res.data[item]
							dictObj[item] = res.data[item]
						}
						commit('SET_DICT_OBJ', dictObj)
						resolve(result)
					}).catch(error => {
						reject(error)
					})
				} else {
					resolve(result)
				}
			})
		}
  }
}

export default dict
