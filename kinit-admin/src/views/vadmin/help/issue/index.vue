<script lang="ts">
export default {
  name: 'HelpIssue'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getIssueListApi,
  delIssueListApi,
  getIssueCategoryOptionsApi
} from '@/api/vadmin/help/issue'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/issue.data'
import { ref, watch, nextTick } from 'vue'
import { ElRow, ElCol, ElButton, ElSwitch } from 'element-plus'
import { RightToolbar } from '@/components/RightToolbar'
import { FormSetPropsType } from '@/types/form'
import { Search } from '@/components/Search'
import { useI18n } from '@/hooks/web/useI18n'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'

const { wsCache } = useCache()
const { t } = useI18n()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getIssueListApi,
  delListApi: delIssueListApi,
  response: {
    data: 'data',
    count: 'count'
  }
})

const { getList, setSearchParams } = methods

const tableSize = ref('default')

watch(tableSize, (val) => {
  tableSize.value = val
})

const { currentRoute, push } = useRouter()
const cacheTableHeadersKey = currentRoute.value.fullPath

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

const searchSetSchemaList = ref([] as FormSetPropsType[])

const getOptions = async () => {
  const res = await getIssueCategoryOptionsApi()
  if (res) {
    searchSetSchemaList.value.push({
      field: 'category_id',
      path: 'componentProps.options',
      value: res.data
    })
  }
}

getOptions()

// 新增类别事件
const auditAction = async () => {
  push('/help/issue/form')
}

// 编辑事件
const updateAction = async (row: any) => {
  push(`/help/issue/form?id=${row.id}`)
}

// 删除事件
const delData = async (row: any) => {
  const { delListApi } = methods
  await delListApi(true, [row.id])
}

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
      <ElRow>
        <ElCol :span="1.5">
          <ElButton type="primary" @click="auditAction">新增问题</ElButton>
        </ElCol>
      </ElRow>
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
      <template #is_active="{ row }">
        <ElSwitch :value="row.is_active" size="small" disabled />
      </template>

      <template #action="{ row }">
        <ElButton type="primary" link size="small" @click="updateAction(row)">
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="danger" link size="small" @click="delData(row)">
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>
    </Table>
  </ContentWrap>
</template>
