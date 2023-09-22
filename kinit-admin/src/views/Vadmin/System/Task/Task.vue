<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getTaskListApi,
  addTaskListApi,
  delTaskListApi,
  putTaskListApi,
  getTaskApi,
  runOnceTaskApi
} from '@/api/vadmin/system/task'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElMessage, ElSwitch, ElRow, ElCol, ElMessageBox } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useRouter } from 'vue-router'
import CronExpression from './components/CronExpression.vue'

defineOptions({
  name: 'SystemTask'
})

const { push } = useRouter()
const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getTaskListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delTaskListApi(value as string)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: '_id',
    label: '任务编号',
    show: true,
    disabled: true,
    width: '230px',
    span: 24
  },
  {
    field: 'name',
    label: '任务名称',
    show: true,
    disabled: true,
    span: 24
  },
  {
    field: 'group',
    label: '任务分组',
    show: true,
    span: 24
  },
  {
    field: 'job_class',
    label: '调用目标',
    show: true,
    span: 24
  },
  {
    field: 'exec_strategy',
    label: '执行策略',
    show: true,
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
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
    field: 'is_active',
    label: '任务状态',
    show: true,
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch value={row.is_active} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'last_run_datetime',
    label: '最近一次执行时间',
    show: true,
    width: '180px',
    span: 24
  },
  {
    field: 'remark',
    label: '任务备注',
    show: true,
    span: 24
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true,
    width: '180px',
    span: 24
  },
  {
    field: 'action',
    label: '操作',
    show: true,
    disabled: false,
    width: '240px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
            </ElButton>
            <ElButton type="primary" link size="small" onClick={() => toRecord(row)}>
              调度日志
            </ElButton>
            <ElButton type="primary" link size="small" onClick={() => runOnceTask(row)}>
              执行一次
            </ElButton>
            <ElButton type="danger" link size="small" onClick={() => delData(row)}>
              删除
            </ElButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '任务名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: '_id',
    label: '任务编号',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'group',
    label: '任务分组',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: []
    }
  }
])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const delLoading = ref(false)

const delData = async (row: any) => {
  delLoading.value = true
  await delList(true, [row._id]).finally(() => {
    delLoading.value = false
  })
}

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

const editAction = async (row: any) => {
  const res = await getTaskApi(row._id)
  if (res) {
    dialogTitle.value = '编辑定时任务'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增定时任务'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addTaskListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putTaskListApi(formData._id, formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      }
    } finally {
      saveLoading.value = false
    }
  }
}

// 生成 cron 表达式
const generateCronExpression = () => {
  dialogTitle.value = 'Cron 表达式'
  actionType.value = 'expression'
  currentRow.value = undefined
  dialogVisible.value = true
}

// 跳转到调度日志页面
const toRecord = (row: any) => {
  if (row) {
    push(`/system/record/task?job_id=${row._id}`)
  } else {
    push(`/system/record/task`)
  }
}

// 执行一次任务
const runOnceTask = async (row: any) => {
  ElMessageBox.confirm('是否确认立即执行一次任务', '提示', {
    confirmButtonText: t('common.delOk'),
    cancelButtonText: t('common.delCancel'),
    type: 'warning'
  }).then(async () => {
    const res = await runOnceTaskApi(row._id)
    if (res) {
      if (res.data > 0) {
        ElMessage.success('任务成功被消费者接收！')
      } else {
        ElMessage.error('执行失败，未有消费者接收任务，请检查定时任务程序状态！')
      }
    }
  })
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
      default-expand-all
      node-key="id"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    >
      <template #toolbar>
        <ElRow :gutter="10">
          <ElCol :span="1.5">
            <ElButton type="primary" @click="addAction">新增定时任务</ElButton>
          </ElCol>
          <ElCol :span="1.5">
            <ElButton type="primary" @click="toRecord(null)">调度日志</ElButton>
          </ElCol>
          <ElCol :span="1.5">
            <ElButton type="primary" @click="generateCronExpression">快速生成 Cron 表达式</ElButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="680" :width="850">
    <Write
      v-if="actionType === 'add' || actionType === 'edit'"
      ref="writeRef"
      :current-row="currentRow"
    />

    <CronExpression v-if="actionType === 'expression'" />

    <template #footer>
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
