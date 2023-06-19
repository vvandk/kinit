<script lang="ts">
export default {
  name: 'SystemSettings'
}
</script>

<script setup lang="ts">
import { ElTabs, ElTabPane } from 'element-plus'
import { ref } from 'vue'
import Basic from './basic.vue'
import Baidu from './baidu.vue'
import Privacy from './privacy.vue'
import Agreement from './agreement.vue'
import WXClient from './wxServer.vue'
import Email from './email.vue'
import { ContentWrap } from '@/components/ContentWrap'
import { getSystemSettingsTabsApi } from '@/api/vadmin/system/settings'

const activeName = ref('web_basic')

const tabs = ref([] as Recordable[])

const getList = async () => {
  const res = await getSystemSettingsTabsApi({ classify: 'web' })
  if (res) {
    tabs.value = res.data
  }
}

getList()
</script>

<template>
  <ContentWrap>
    <ElTabs v-model="activeName">
      <template v-for="item in tabs" :key="item.id">
        <ElTabPane v-if="!item.hidden" :name="item.tab_name" :label="item.tab_label">
          <Basic v-if="item.tab_name === 'web_basic'" :tab-id="item.id" />
          <Baidu v-else-if="item.tab_name === 'web_baidu'" :tab-id="item.id" />
          <Privacy v-else-if="item.tab_name === 'web_privacy'" :tab-id="item.id" />
          <Agreement v-else-if="item.tab_name === 'web_agreement'" :tab-id="item.id" />
          <WXClient v-else-if="item.tab_name === 'wx_server'" :tab-id="item.id" />
          <Email v-else-if="item.tab_name === 'web_email'" :tab-id="item.id" />
        </ElTabPane>
      </template>
    </ElTabs>
  </ContentWrap>
</template>

<style scoped lang="less"></style>
