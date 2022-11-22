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

watch(
  columns,
  async () => {
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
    <Search :schema="searchSchema" @search="setSearchParams" @reset="setSearchParams" />

    <div class="mb-8px flex justify-between">
      <ElRow />
      <RightToolbar @get-list="getList" v-model:table-size="tableSize" v-model:columns="columns" />
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
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="900px">
      <Detail :detail-schema="columns" :current-row="tableObject.currentRow" />
    </Dialog>
  </ContentWrap>
</template>
