<script lang="ts">
export default {
  name: 'HelpIssue'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getIssueCategoryListApi,
  addIssueCategoryApi,
  getIssueCategoryApi,
  delIssueCategoryListApi,
  putIssueCategoryApi
} from '@/api/vadmin/help/issue'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/issueCategory.data'
import { ref, watch, nextTick, unref } from 'vue'
import { ElRow, ElCol, ElButton, ElSwitch } from 'element-plus'
import { RightToolbar } from '@/components/RightToolbar'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { FormSetPropsType } from '@/types/form'
import { Search } from '@/components/Search'
import { useI18n } from '@/hooks/web/useI18n'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'

const { wsCache } = useCache()
const { t } = useI18n()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getIssueCategoryListApi,
  delListApi: delIssueCategoryListApi,
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

const dialogVisible = ref(false)
const dialogTitle = ref('')
const loading = ref(false)
const actionType = ref('')
const platformOptions = ref<DictDetail[]>([])
const searchSetSchemaList = ref([] as FormSetPropsType[])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_platform'])
  platformOptions.value = dictOptions.sys_vadmin_platform
  searchSetSchemaList.value.push({
    field: 'platform',
    path: 'componentProps.options',
    value: dictOptions.sys_vadmin_platform
  })
}

getOptions()

// 新增类别事件
const addAction = async () => {
  dialogTitle.value = '新增类别'
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = async (row: any) => {
  const res = await getIssueCategoryApi(row.id)
  if (res) {
    dialogTitle.value = '编辑'
    tableObject.currentRow = res.data
    dialogVisible.value = true
    actionType.value = 'edit'
  }
}

// 删除事件
const delData = async (row: any) => {
  const { delListApi } = methods
  await delListApi(true, [row.id])
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
        const res = ref({})
        if (actionType.value === 'add') {
          res.value = await addIssueCategoryApi(data)
          if (res.value) {
            dialogVisible.value = false
            getList()
          }
        } else if (actionType.value === 'edit') {
          res.value = await putIssueCategoryApi(data)
          if (res.value) {
            dialogVisible.value = false
            getList()
          }
        }
      } finally {
        loading.value = false
      }
    }
  })
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
          <ElButton type="primary" @click="addAction">新增类别</ElButton>
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

      <template #platform="{ row }">
        {{ selectDictLabel(platformOptions, row.platform) }}
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

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <Write
        ref="writeRef"
        :current-row="tableObject.currentRow"
        :platform-options="platformOptions"
      />

      <template #footer>
        <ElButton type="primary" :loading="loading" @click="save">
          {{ t('exampleDemo.save') }}
        </ElButton>
        <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
      </template>
    </Dialog>
  </ContentWrap>
</template>
