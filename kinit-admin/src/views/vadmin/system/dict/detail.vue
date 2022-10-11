<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getDictDetailsListApi,
  addDictDetailsListApi,
  delDictDetailsListApi,
  putDictDetailsListApi,
  getDictDetailsApi,
  getDictTypeOptionsApi
} from '@/api/vadmin/system/dict'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/detail.data'
import { ref, unref } from 'vue'
import Write from './components/DetailWrite.vue'
import { Dialog } from '@/components/Dialog'
import { ElButton, ElMessage } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { useRouter } from 'vue-router'
import { Search } from '@/components/Search'

const { currentRoute } = useRouter()

const { t } = useI18n()

let dictType = currentRoute.value.query.dictType

const searchSetSchemaList = ref([] as FormSetPropsType[])

const getOptions = async () => {
  const res = await getDictTypeOptionsApi()
  searchSetSchemaList.value.push({
    field: 'dict_type_id',
    path: 'componentProps.options',
    value: res.data
  })
}

getOptions()

if (typeof dictType === 'string') {
  searchSetSchemaList.value.push({
    field: 'dict_type_id',
    path: 'value',
    value: parseInt(dictType)
  })
}

const { register, tableObject, methods } = useTable({
  getListApi: getDictDetailsListApi,
  delListApi: delDictDetailsListApi,
  response: {
    data: 'data',
    count: 'count'
  },
  props: {
    columns
  }
})
tableObject.params = { dict_type_id: dictType }

const dialogVisible = ref(false)
const dialogTitle = ref('')
const actionType = ref('')
const loading = ref(false)

// 添加事件
const AddAction = () => {
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = async (row: any) => {
  const res = await getDictDetailsApi(row.id)
  dialogTitle.value = '编辑'
  tableObject.currentRow = res.data
  dialogVisible.value = true
  actionType.value = 'edit'
}

// 删除事件
const delData = async (row: any) => {
  tableObject.currentRow = row
  const { delListApi } = methods
  loading.value = true
  await delListApi([row.id], false).finally(() => {
    loading.value = false
  })
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
      data.dict_type_id = dictType
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addDictDetailsListApi(data)
      } else if (actionType.value === 'edit') {
        res.value = await putDictDetailsListApi(data)
      }
      if (res.value) {
        dialogVisible.value = false
        getList()
      }
      loading.value = false
    }
  })
}

const { getList, setSearchParams } = methods

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

    <div class="mb-10px">
      <ElButton type="primary" @click="AddAction">{{ t('exampleDemo.add') }}</ElButton>
    </div>

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
      <template #action="{ row }">
        <ElButton type="primary" text size="small" @click="updateAction(row)">
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="danger" text size="small" @click="delData(row)">
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
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
