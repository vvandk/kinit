<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getIssueCategoryListApi,
  addIssueCategoryApi,
  getIssueCategoryApi,
  delIssueCategoryListApi,
  putIssueCategoryApi
} from '@/api/vadmin/help/issue'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'

defineOptions({
  name: 'HelpIssueCategory'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getIssueCategoryListApi({
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
    const res = await delIssueCategoryListApi(value)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const platformOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_platform'])
  platformOptions.value = dictOptions.sys_vadmin_platform
}

getOptions()

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    show: true,
    disabled: true
  },
  {
    field: 'name',
    label: '类别名称',
    show: true,
    disabled: true
  },
  {
    field: 'platform',
    label: '展示平台',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>{selectDictLabel(platformOptions.value, row.platform)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'is_active',
    label: '是否可见',
    show: true,
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
    field: 'create_datetime',
    label: '创建时间',
    show: true,
    sortable: true
  },
  {
    field: 'create_user.name',
    label: '创建人',
    show: true
  },
  {
    field: 'action',
    width: '120px',
    label: '操作',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
            </ElButton>
            <ElButton
              type="danger"
              loading={delLoading.value}
              link
              size="small"
              onClick={() => delData(row)}
            >
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
    label: '类别名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'platform',
    label: '登录平台',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: []
    }
  },
  {
    field: 'is_active',
    label: '是否可见',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '可见',
          value: true
        },
        {
          label: '不可见',
          value: false
        }
      ]
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
  await delList(true, [row.id]).finally(() => {
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
  const res = await getIssueCategoryApi(row.id)
  if (res) {
    dialogTitle.value = '编辑常见问题类别'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增常见问题类别'
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
        res.value = await addIssueCategoryApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putIssueCategoryApi(formData)
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
            <ElButton type="primary" @click="addAction">新增常见问题类别</ElButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="650">
    <Write ref="writeRef" :current-row="currentRow" />

    <template #footer>
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
