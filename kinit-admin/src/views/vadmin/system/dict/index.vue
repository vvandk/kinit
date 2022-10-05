<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getDictTypeListApi,
  addDictTypeListApi,
  delDictTypeListApi,
  putDictTypeListApi,
  getDictTypeApi
} from '@/api/vadmin/system/dict'
import { useTable } from '@/hooks/web/useTable'
import { columns } from './components/dict.data'
import { ref, unref } from 'vue'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { ElButton, ElMessage } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'

const { t } = useI18n()

const { register, tableObject, methods } = useTable({
  getListApi: getDictTypeListApi,
  delListApi: delDictTypeListApi,
  response: {
    data: 'data',
    count: 'count'
  },
  props: {
    columns
  }
})

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
  const res = await getDictTypeApi(row.id)
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
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addDictTypeListApi(data)
      } else if (actionType.value === 'edit') {
        res.value = await putDictTypeListApi(data)
      }
      if (res.value) {
        dialogVisible.value = false
        getList()
      }
      loading.value = false
    }
  })
}

const { getList } = methods

getList()
</script>

<template>
  <ContentWrap>
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
