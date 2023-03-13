<script lang="ts">
export default {
  name: 'SystemRecordLogin'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { getRecordLoginListApi } from '@/api/vadmin/system/record/login'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/login.data'
import { ref, watch, nextTick } from 'vue'
import { ElButton, ElSwitch, ElRow } from 'element-plus'
import { RightToolbar } from '@/components/RightToolbar'
import { Dialog } from '@/components/Dialog'
import Detail from './components/Detail.vue'
import { Search } from '@/components/Search'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import { FormSetPropsType } from '@/types/form'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'

const { wsCache } = useCache()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getRecordLoginListApi,
  response: {
    data: 'data',
    count: 'count'
  },
  defaultParams: {
    v_order: 'descending',
    v_order_field: 'create_datetime'
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const platformOptions = ref<DictDetail[]>([])
const loginMethodOptions = ref<DictDetail[]>([])
const searchSetSchemaList = ref([] as FormSetPropsType[])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_platform', 'sys_vadmin_login_method'])
  platformOptions.value = dictOptions.sys_vadmin_platform
  loginMethodOptions.value = dictOptions.sys_vadmin_login_method
  searchSetSchemaList.value.push({
    field: 'platform',
    path: 'componentProps.options',
    value: dictOptions.sys_vadmin_platform
  })
}

getOptions()

const view = (row: any) => {
  dialogTitle.value = '登录详情'
  tableObject.currentRow = row
  dialogVisible.value = true
}

const { getList, setSearchParams, setOrderParams } = methods

const tableSize = ref('default')

watch(tableSize, (val) => {
  tableSize.value = val
})

const route = useRouter()
const cacheTableHeadersKey = route.currentRoute.value.fullPath

watch(
  columns,
  async (val) => {
    wsCache.set(cacheTableHeadersKey, JSON.stringify(val))
    await nextTick()
    elTableRef.value?.doLayout()
  },
  {
    deep: true
  }
)

getList()
</script>

<template>
  <ContentWrap>
    <Search
      :schema="searchSchema"
      :setSchemaList="searchSetSchemaList"
      @search="setSearchParams"
      @reset="setSearchParams"
    />

    <div class="mb-8px flex justify-between">
      <ElRow />
      <RightToolbar
        @get-list="getList"
        v-model:table-size="tableSize"
        v-model:columns="columns"
        :cache-table-headers-key="cacheTableHeadersKey"
      />
    </div>

    <Table
      v-model:limit="tableObject.limit"
      v-model:page="tableObject.page"
      :defaultSort="{ prop: 'create_datetime', order: 'descending' }"
      :columns="columns"
      :data="tableObject.tableData"
      :loading="tableObject.loading"
      :selection="false"
      :size="tableSize"
      :border="true"
      :pagination="{
        total: tableObject.count
      }"
      @register="register"
      @sort-change="setOrderParams"
    >
      <template #action="{ row }">
        <ElButton type="primary" link size="small" @click="view(row)"> 详情 </ElButton>
      </template>

      <template #status="{ row }">
        <ElSwitch :value="row.status" size="small" disabled />
      </template>

      <template #platform="{ row }">
        {{ selectDictLabel(platformOptions, row.platform) }}
      </template>

      <template #login_method="{ row }">
        {{ selectDictLabel(loginMethodOptions, row.login_method) }}
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="900px">
      <Detail :detail-schema="columns" :current-row="tableObject.currentRow" />
    </Dialog>
  </ContentWrap>
</template>
