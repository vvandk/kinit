<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { getTableListApi } from '@/api/table'
import { TableData } from '@/api/table/types'
import { reactive } from 'vue'
import { useTable } from '@/hooks/web/useTable'

const columns = reactive<TableColumn[]>([
  {
    field: 'index',
    label: 'index',
    type: 'index'
  },
  {
    field: 'title',
    label: 'title'
  },
  {
    field: 'author',
    label: 'author'
  },
  {
    field: 'display_time',
    label: 'displayTime'
  },
  {
    field: 'pageviews',
    label: 'pageviews'
  },
  {
    field: 'action',
    label: 'action'
  }
])

const { register, tableObject, methods } = useTable<TableData>({
  getListApi: getTableListApi,
  response: {
    list: 'list',
    total: 'total'
  },
  props: {
    columns
  }
})

const { getList } = methods

getList()
</script>

<template>
  <ContentWrap>
    <Table
      v-model:pageSize="tableObject.pageSize"
      v-model:currentPage="tableObject.currentPage"
      :data="tableObject.tableList"
      :loading="tableObject.loading"
      :pagination="{
        total: tableObject.total
      }"
      @register="register"
    />
  </ContentWrap>
</template>
