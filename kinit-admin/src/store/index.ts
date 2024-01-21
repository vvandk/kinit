import type { App } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// pinia-plugin-persistedstate 持久化存储官方文档：https://prazdevs.github.io/pinia-plugin-persistedstate/zh/guide/

const store = createPinia()

store.use(piniaPluginPersistedstate)

export const setupStore = (app: App<Element>) => {
  app.use(store)
}

export { store }
