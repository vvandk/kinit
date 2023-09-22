<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getRecordOperationListApi } from '@/api/vadmin/system/record/operation'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Detail from './components/Detail.vue'
import { Dialog } from '@/components/Dialog'

defineOptions({
  name: 'SystemRecordOperation'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getRecordOperationListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'user_id',
    label: '操作人编号',
    show: true,
    disabled: true,
    width: '100px'
  },
  {
    field: 'user_name',
    label: '操作人',
    show: true,
    disabled: true,
    width: '100px'
  },
  {
    field: 'telephone',
    label: '手机号',
    show: true,
    disabled: true,
    width: '130px'
  },
  {
    field: 'request_method',
    label: '请求方法',
    show: true,
    disabled: true,
    width: '100px'
  },
  {
    field: 'client_ip',
    label: '客户端地址',
    width: '130px',
    show: true,
    disabled: true
  },
  {
    field: 'tags',
    label: '标签',
    width: '130px',
    show: true
  },
  {
    field: 'summary',
    label: '操作内容',
    show: true
  },
  {
    field: 'description',
    label: '描述',
    show: false
  },
  {
    field: 'status_code',
    label: '操作状态',
    show: true,
    width: '100px'
  },
  {
    field: 'route_name',
    label: '接口函数',
    show: false,
    width: '150px'
  },
  {
    field: 'api_path',
    label: '接口地址',
    show: false
  },
  {
    field: 'params',
    label: '请求参数',
    show: false
  },
  {
    field: 'browser',
    label: '浏览器',
    show: true,
    width: '150px'
  },
  {
    field: 'system',
    label: '系统',
    show: false,
    width: '150px'
  },
  {
    field: 'process_time',
    label: '总耗时',
    show: true
  },
  {
    field: 'create_datetime',
    label: '操作时间',
    show: true
  },
  {
    field: 'action',
    width: '100px',
    show: true,
    label: '操作',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link onClick={() => action(row, 'detail')}>
              详情
            </ElButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'telephone',
    label: '手机号',
    component: 'Input',
    componentProps: {
      clearable: false
    }
  },
  {
    field: 'request_method',
    label: '请求方法',
    component: 'Input',
    componentProps: {
      clearable: false
    }
  },
  {
    field: 'summary',
    label: '操作内容',
    component: 'Input',
    componentProps: {
      clearable: false
    }
  }
])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const action = (row: any, type: string) => {
  dialogTitle.value = t('exampleDemo.detail')
  actionType.value = type
  currentRow.value = row
  dialogVisible.value = true
}
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      :columns="tableColumns"
      node-key="id"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    />
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
    <Detail v-if="actionType === 'detail'" :current-row="currentRow" />

    <template #footer>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
