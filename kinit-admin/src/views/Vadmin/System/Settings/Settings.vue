<script setup lang="ts">
import { ElTabs, ElTabPane } from 'element-plus'
import { ref } from 'vue'
import Basic from './components/Basic.vue'
import Privacy from './components/Privacy.vue'
import Agreement from './components/Agreement.vue'
import WXClient from './components/WechatServer.vue'
import Email from './components/Email.vue'
import SMS from './components/SMS.vue'
import { ContentWrap } from '@/components/ContentWrap'
import { getSystemSettingsTabsApi } from '@/api/vadmin/system/settings'

defineOptions({
  name: 'SystemSettings'
})

const activeName = ref('web_basic')

const tabs = ref([] as Recordable[])

const getList = async () => {
  const res = await getSystemSettingsTabsApi(['web', 'aliyun'])
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
          <Privacy v-else-if="item.tab_name === 'web_privacy'" :tab-id="item.id" />
          <Agreement v-else-if="item.tab_name === 'web_agreement'" :tab-id="item.id" />
          <WXClient v-else-if="item.tab_name === 'wx_server'" :tab-id="item.id" />
          <Email v-else-if="item.tab_name === 'web_email'" :tab-id="item.id" />
          <SMS v-else-if="item.tab_name === 'aliyun_sms'" :tab-id="item.id" />
        </ElTabPane>
      </template>
    </ElTabs>
  </ContentWrap>
</template>

<style scoped lang="less"></style>
