<script lang="ts">
export default {
  name: 'SystemRecordTask'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { getTaskRecordListApi } from '@/api/vadmin/system/task'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/task.data'
import { ref, watch, nextTick } from 'vue'
import { ElButton, ElRow } from 'element-plus'
import { RightToolbar } from '@/components/RightToolbar'
import { Dialog } from '@/components/Dialog'
import Detail from './components/Detail.vue'
import { Search } from '@/components/Search'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'
import { DictDetail, selectDictLabel } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import { FormSetPropsType } from '@/types/form'

const { wsCache } = useCache()
const { currentRoute } = useRouter()

const job_id = currentRoute.value.query.job_id

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getTaskRecordListApi,
  response: {
    data: 'data',
    count: 'count'
  }
})
tableObject.params = { job_id: job_id }

const dialogVisible = ref(false)
const dialogTitle = ref('')
const execStrategyOptions = ref<DictDetail[]>([])
const searchSetSchemaList = ref([] as FormSetPropsType[])

if (typeof job_id === 'string') {
  searchSetSchemaList.value.push({
    field: 'job_id',
    path: 'value',
    value: job_id
  })
}

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['vadmin_system_task_exec_strategy'])
  execStrategyOptions.value = dictOptions.vadmin_system_task_exec_strategy
}

getOptions()

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
      <template #exec_strategy="{ row }">
        {{ selectDictLabel(execStrategyOptions, row.exec_strategy) }}
      </template>

      <template #action="{ row }">
        <ElButton type="primary" link size="small" @click="view(row)"> 详情 </ElButton>
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="900px">
      <Detail :detail-schema="columns" :current-row="tableObject.currentRow" />
    </Dialog>
  </ContentWrap>
</template>
