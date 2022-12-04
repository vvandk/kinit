import Vue from 'vue'
import Vuex from 'vuex'
import auth from '@/store/modules/auth'
import app from '@/store/modules/app'
import dict from '@/store/modules/dict'
import getters from './getters'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    auth,
		app,
		dict
  },
  getters
})

export default store
