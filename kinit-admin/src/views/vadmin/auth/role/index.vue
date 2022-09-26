<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { getRoleListApi } from '@/api/vadmin/auth/role'
import { TableData } from '@/api/table/types'
import { reactive } from 'vue'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { ElButton } from 'element-plus'

const { t } = useI18n()

const columns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '角色编号'
  },
  {
    field: 'name',
    label: '角色名称'
  },
  {
    field: 'role_key',
    label: '权限字符'
  },
  {
    field: 'index',
    label: '显示顺序'
  },
  {
    field: 'is_active',
    label: '状态'
  },
  {
    field: 'is_admin',
    label: '最高权限'
  },
  {
    field: 'create_datetime',
    label: '创建时间'
  },
  {
    field: 'action',
    width: '260px',
    label: t('tableDemo.action'),
    form: {
      show: false
    },
    detail: {
      show: false
    }
  }
])

const { register, tableObject, methods } = useTable<TableData>({
  getListApi: getRoleListApi,
  response: {
    data: 'data',
    count: 'count'
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
      v-model:limit="tableObject.limit"
      v-model:page="tableObject.page"
      :data="tableObject.tableData"
      :loading="tableObject.loading"
      :selection="false"
      :pagination="{
        total: tableObject.count
      }"
      @register="register"
    >
      <template #action="{}">
        <ElButton type="primary" text>
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="success" text>
          {{ t('exampleDemo.detail') }}
        </ElButton>
        <ElButton type="danger" text>
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>
    </Table>
  </ContentWrap>
</template>
