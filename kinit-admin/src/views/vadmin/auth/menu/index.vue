<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { getMenuListApi, delMenuListApi } from '@/api/vadmin/auth/menu'
import { TableData } from '@/api/table/types'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { ElButton, ElTag } from 'element-plus'
import { h, ref, unref, reactive } from 'vue'
import { Dialog } from '@/components/Dialog'
import Write from './components/Write.vue'

const { t } = useI18n()

const columns = reactive<TableColumn[]>([
  {
    field: 'title',
    label: '菜单名称'
  },
  {
    field: 'icon',
    label: '图标'
  },
  {
    field: 'order',
    label: '排序'
  },
  {
    field: 'menu_type',
    label: '菜单类型'
  },
  {
    field: 'perms',
    label: '权限标识'
  },
  {
    field: 'component',
    label: '组件路径'
  },
  {
    field: 'action',
    width: '260px',
    label: t('tableDemo.action'),
    form: {
      show: false
    }
  }
])

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
const actionType = ref('')
const delLoading = ref(false)

const AddAction = () => {
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = ''
}

const delData = async (row: TableData | null, multiple: boolean) => {
  tableObject.currentRow = row
  const { delListApi, getSelections } = methods
  const selections = await getSelections()
  delLoading.value = true
  await delListApi(
    multiple ? selections.map((v) => v.id) : [tableObject.currentRow?.id as string],
    multiple
  ).finally(() => {
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
      const data = (await write?.getFormData()) as TableData
      console.log('a', data)
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
      @register="register"
    >
      <template #action="{}">
        <ElButton type="primary" text>
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="danger" text>
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
