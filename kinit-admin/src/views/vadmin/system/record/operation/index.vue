<script lang="ts">
export default {
  name: 'SystemRecordOperation'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { getRecordOperationListApi } from '@/api/vadmin/system/record/operation'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/operation.data'
import { ref, watch, nextTick } from 'vue'
import { ElButton, ElSwitch, ElRow } from 'element-plus'
import { RightToolbar } from '@/components/RightToolbar'
import { Dialog } from '@/components/Dialog'
import Detail from './components/Detail.vue'
import { Search } from '@/components/Search'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'

const { wsCache } = useCache()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getRecordOperationListApi,
  response: {
    data: 'data',
    count: 'count'
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')

const view = (row: any) => {
  dialogTitle.value = '操作记录'
  tableObject.currentRow = row
  dialogVisible.value = true
}

const { getList, setSearchParams } = methods

getList()

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
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @search="setSearchParams" @reset="setSearchParams" />

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
    >
      <template #action="{ row }">
        <ElButton type="primary" link size="small" @click="view(row)"> 详情 </ElButton>
      </template>

      <template #status="{ row }">
        <ElSwitch :value="row.status" size="small" disabled />
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="900px">
      <Detail :detail-schema="columns" :current-row="tableObject.currentRow" />
    </Dialog>
  </ContentWrap>
</template>
