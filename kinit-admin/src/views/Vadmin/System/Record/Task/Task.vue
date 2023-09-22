<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Detail from './components/Detail.vue'
import { Dialog } from '@/components/Dialog'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import { useRouter } from 'vue-router'
import { getTaskRecordListApi } from '@/api/vadmin/system/task'

defineOptions({
  name: 'SystemRecordTask'
})

const { t } = useI18n()
const { currentRoute } = useRouter()

const job_id = currentRoute.value.query.job_id

const execStrategyOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['vadmin_system_task_exec_strategy'])
  execStrategyOptions.value = dictOptions.vadmin_system_task_exec_strategy
}

getOptions()

const { tableRegister, tableState, tableMethods } = useTable({
  immediate: false,
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getTaskRecordListApi({
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
    field: 'job_id',
    label: '任务编号',
    show: true,
    disabled: true,
    width: '240px'
  },
  {
    field: 'name',
    label: '任务名称',
    show: true,
    disabled: true
  },
  {
    field: 'group',
    label: '任务分组',
    show: true,
    span: 2
  },
  {
    field: 'job_class',
    label: '调用目标',
    show: true
  },
  {
    field: 'exec_strategy',
    label: '执行策略',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>{selectDictLabel(execStrategyOptions.value, row.exec_strategy)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'expression',
    label: '表达式',
    show: true,
    span: 24
  },
  {
    field: 'start_time',
    label: '开始执行时间',
    show: false,
    width: '200px'
  },
  {
    field: 'end_time',
    label: '执行完成时间',
    width: '200px',
    show: true
  },
  {
    field: 'process_time',
    label: '耗时(秒)',
    width: '110px',
    show: true
  },
  {
    field: 'retval',
    label: '任务返回值',
    show: true
  },
  {
    field: 'exception',
    label: '异常信息',
    show: false,
    span: 24
  },
  {
    field: 'traceback',
    label: '堆栈跟踪',
    show: false,
    width: '100px'
  },
  {
    field: 'action',
    width: '100px',
    label: '操作',
    show: true,
    disabled: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => view(row)}>
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
    field: 'job_id',
    label: '任务编号',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '240px'
      }
    },
    value: job_id
  },
  {
    field: 'name',
    label: '任务名称',
    component: 'Input',
    componentProps: {
      clearable: true
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

const view = (row) => {
  dialogTitle.value = t('exampleDemo.detail')
  actionType.value = 'detail'
  currentRow.value = row
  dialogVisible.value = true
}

if (job_id) {
  searchParams.value = { job_id: job_id }
  getList()
} else {
  getList()
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
