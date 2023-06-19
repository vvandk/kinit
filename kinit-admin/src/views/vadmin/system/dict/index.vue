<script lang="ts">
export default {
  name: 'SystemDict'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { RightToolbar } from '@/components/RightToolbar'
import {
  getDictTypeListApi,
  addDictTypeListApi,
  delDictTypeListApi,
  putDictTypeListApi,
  getDictTypeApi
} from '@/api/vadmin/system/dict'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/dict.data'
import { ref, unref, watch, nextTick } from 'vue'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { ElButton, ElMessage, ElRow, ElCol } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { useRouter } from 'vue-router'
import { Search } from '@/components/Search'
import { useCache } from '@/hooks/web/useCache'
import { useClipboard } from '@vueuse/core'

const { wsCache } = useCache()
const { push } = useRouter()
const { t } = useI18n()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getDictTypeListApi,
  delListApi: delDictTypeListApi,
  response: {
    data: 'data',
    count: 'count'
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const actionType = ref('')
const loading = ref(false)

// 添加事件
const addAction = () => {
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = async (row: any) => {
  const res = await getDictTypeApi(row.id)
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

// 跳转到字典详情页面
const toDetail = (row: any) => {
  push(`/system/dict/detail?dictType=${row.id}`)
}

// 复制字典类型
const toCopy = async (value: string) => {
  const { copy } = useClipboard()
  await copy(value)
  return ElMessage.success('复制成功')
}

const writeRef = ref<ComponentRef<typeof Write>>()

const save = async () => {
  const write = unref(writeRef)
  await write?.elFormRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      let data = await write?.getFormData()
      if (!data) {
        loading.value = false
        return ElMessage.error('未获取到数据')
      }
      const res = ref({})
      try {
        if (actionType.value === 'add') {
          res.value = await addDictTypeListApi(data)
          if (res.value) {
            dialogVisible.value = false
            getList()
          }
        } else if (actionType.value === 'edit') {
          res.value = await putDictTypeListApi(data)
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
    <Search :schema="searchSchema" @search="setSearchParams" @reset="setSearchParams" />

    <div class="mb-8px flex justify-between">
      <ElRow :gutter="10">
        <ElCol :span="1.5">
          <ElButton type="primary" @click="addAction">{{ t('exampleDemo.add') }}</ElButton>
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
      :pagination="{
        total: tableObject.count
      }"
      :border="true"
      :size="tableSize"
      @register="register"
    >
      <template #action="{ row }">
        <ElButton type="primary" link size="small" @click="updateAction(row)">
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="danger" link size="small" @click="delData(row)">
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>

      <template #dict_type="{ row }">
        <Icon
          icon="material-symbols:content-copy-rounded"
          class="cursor-pointer"
          @click="toCopy(row.dict_type)"
        />
        <ElButton type="primary" link @click="toDetail(row)">
          {{ row.dict_type }}
        </ElButton>
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <Write ref="writeRef" :current-row="tableObject.currentRow" />

      <template #footer>
        <ElButton type="primary" :loading="loading" @click="save">
          {{ t('exampleDemo.save') }}
        </ElButton>
        <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
      </template>
    </Dialog>
  </ContentWrap>
</template>
