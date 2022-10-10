<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getMenuListApi,
  delMenuListApi,
  addMenuListApi,
  putMenuListApi
} from '@/api/vadmin/auth/menu'
import { TableData } from '@/api/table/types'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { ElButton, ElSwitch } from 'element-plus'
import { ref, unref } from 'vue'
import { Dialog } from '@/components/Dialog'
import Write from './components/Write.vue'
import { columns } from './components/menu.data'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'

const { t } = useI18n()

let menuTypeOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_menu_type'])
  menuTypeOptions.value = dictOptions.sys_vadmin_menu_type
}

getOptions()

const { register, tableObject, methods } = useTable<TableData>({
  getListApi: getMenuListApi,
  delListApi: delMenuListApi,
  response: {
    data: 'data'
  },
  props: {
    columns
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const delLoading = ref(false)
const actionType = ref('')

// 添加事件
const AddAction = () => {
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = (row: any) => {
  dialogTitle.value = '编辑'
  tableObject.currentRow = row
  dialogVisible.value = true
  actionType.value = 'edit'
}

// 删除事件
const delData = async (row: any) => {
  tableObject.currentRow = row
  const { delListApi } = methods
  delLoading.value = true
  await delListApi([row.id], false).finally(() => {
    delLoading.value = false
  })
}

const loading = ref(false)

const writeRef = ref<ComponentRef<typeof Write>>()

const save = async () => {
  const write = unref(writeRef)
  await write?.elFormRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      const data = await write?.getFormData()
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addMenuListApi(data)
      } else if (actionType.value === 'edit') {
        res.value = await putMenuListApi(data)
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
      :data="tableObject.tableData"
      :loading="tableObject.loading"
      :selection="false"
      row-key="id"
      default-expand-all
      @register="register"
    >
      <template #title="{ row }">
        {{ t(row.title) }}
      </template>
      <template #icon="{ row }">
        <div v-if="row.icon">
          <Icon :icon="row.icon" />
        </div>
      </template>
      <template #action="{ row }">
        <ElButton type="primary" text size="small" @click="updateAction(row)">
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="danger" text size="small" @click="delData(row)">
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>

      <template #menu_type="{ row }">
        <span>
          {{ selectDictLabel(menuTypeOptions, row.menu_type) }}
        </span>
      </template>

      <template #hidden="{ row }">
        <ElSwitch :value="!row.hidden" disabled />
      </template>

      <template #disabled="{ row }">
        <ElSwitch :value="!row.disabled" disabled />
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
