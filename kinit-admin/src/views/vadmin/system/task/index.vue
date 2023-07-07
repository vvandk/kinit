<script lang="ts">
export default {
  name: 'HelpTask'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getTaskListApi,
  addTaskListApi,
  delTaskListApi,
  putTaskListApi,
  getTaskApi,
  getTaskGroupOptionsApi,
  runOnceTaskApi
} from '@/api/vadmin/system/task'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/task.data'
import { ref, watch, nextTick, unref } from 'vue'
import { ElRow, ElCol, ElButton, ElSwitch, ElMessageBox, ElMessage } from 'element-plus'
import { RightToolbar } from '@/components/RightToolbar'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { FormSetPropsType } from '@/types/form'
import { Search } from '@/components/Search'
import { useI18n } from '@/hooks/web/useI18n'
import { Dialog } from '@/components/Dialog'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'
import Write from './components/Write.vue'
import CronExpression from './components/CronExpression.vue'

const { wsCache } = useCache()
const { t } = useI18n()
const { push } = useRouter()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getTaskListApi,
  delListApi: delTaskListApi,
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

const cronDialogVisible = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const loading = ref(false)
const actionType = ref('')
const execStrategyOptions = ref<DictDetail[]>([])
const taskGroupOptions = ref<DictDetail[]>([])
const searchSetSchemaList = ref([] as FormSetPropsType[])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['vadmin_system_task_exec_strategy'])
  execStrategyOptions.value = dictOptions.vadmin_system_task_exec_strategy
  const res = await getTaskGroupOptionsApi()
  taskGroupOptions.value = res.data.map((item) => {
    return {
      label: item.value,
      value: item.value
    }
  })
  searchSetSchemaList.value.push({
    field: 'group',
    path: 'componentProps.options',
    value: taskGroupOptions.value
  })
}

getOptions()

// 跳转到调度日志页面
const toRecord = (row: any) => {
  if (row) {
    push(`/system/record/task?job_id=${row._id}`)
  } else {
    push(`/system/record/task`)
  }
}

// 添加定时任务事件
const addAction = async () => {
  dialogTitle.value = '添加定时任务'
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = async (row: any) => {
  const res = await getTaskApi(row._id)
  if (res) {
    dialogTitle.value = '编辑定时任务'
    tableObject.currentRow = res.data
    dialogVisible.value = true
    actionType.value = 'edit'
  }
}

// 删除事件
const delData = async (row: any) => {
  const { delListApi } = methods
  await delListApi(false, row._id)
}

// 执行一次任务
const runOnceTask = async (row: any) => {
  ElMessageBox.confirm('是否确认立即执行一次任务', t('common.delWarning'), {
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

const writeRef = ref<ComponentRef<typeof Write>>()

// 提交事件
const save = async () => {
  const write = unref(writeRef)
  await write?.elFormRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      let data = await write?.getFormData()
      try {
        const res = ref({} as any)
        if (data?.exec_strategy === 'date') {
          data.start_date = null
          data.end_date = null
        }
        if (actionType.value === 'add') {
          res.value = await addTaskListApi(data)
          if (res.value) {
            dialogVisible.value = false
            const result = res.value.data
            if (result.is_active) {
              if (result.subscribe_number > 0) {
                ElMessage.success('创建成功，任务成功被消费者接收！')
              } else {
                ElMessage.info('创建成功，未有消费者接收任务，请检查定时任务程序状态！')
              }
            } else {
              ElMessage.success('创建成功！')
            }
            getList()
          }
        } else if (actionType.value === 'edit') {
          res.value = await putTaskListApi(data?._id, data)
          if (res.value) {
            dialogVisible.value = false
            const result = res.value.data
            if (result.is_active) {
              if (result.subscribe_number > 0) {
                ElMessage.success('更新成功，任务已重新被消费者接收！')
              } else {
                ElMessage.info('更新成功，未有消费者接收任务，请检查定时任务程序状态！')
              }
            } else {
              ElMessage.success('更新成功！')
            }
            getList()
          }
        }
      } finally {
        loading.value = false
      }
    }
  })
}

// 生成 cron 表达式
const generateCronExpression = () => {
  cronDialogVisible.value = true
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
          <ElButton type="primary" @click="addAction">添加定时任务</ElButton>
          <ElButton type="primary" @click="toRecord(null)">调度日志</ElButton>
          <ElButton type="primary" @click="generateCronExpression">快速生成 Cron 表达式</ElButton>
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

      <template #exec_strategy="{ row }">
        {{ selectDictLabel(execStrategyOptions, row.exec_strategy) }}
      </template>

      <template #action="{ row }">
        <ElButton type="primary" link size="small" @click="updateAction(row)">
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="primary" link size="small" @click="toRecord(row)"> 调度日志 </ElButton>
        <ElButton type="primary" link size="small" @click="runOnceTask(row)"> 执行一次 </ElButton>
        <ElButton type="danger" link size="small" @click="delData(row)">
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <Write
        ref="writeRef"
        :current-row="tableObject.currentRow"
        :exec-strategy-options="execStrategyOptions"
        :task-group-options="taskGroupOptions"
      />

      <template #footer>
        <ElButton type="primary" :loading="loading" @click="save">
          {{ t('exampleDemo.save') }}
        </ElButton>
        <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
      </template>
    </Dialog>

    <Dialog v-model="cronDialogVisible" title="快速生成 Cron 表达式" width="920px" height="680px">
      <CronExpression />
    </Dialog>
  </ContentWrap>
</template>
