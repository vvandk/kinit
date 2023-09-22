<script setup lang="tsx">
import { reactive, ref, unref, watch } from 'vue'
import {
  getDictDetailsListApi,
  addDictDetailsListApi,
  delDictDetailsListApi,
  putDictDetailsListApi,
  getDictDetailsApi
} from '@/api/vadmin/system/dict'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { propTypes } from '@/utils/propTypes'

const props = defineProps({
  dictTypeId: propTypes.number.def(undefined)
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getDictDetailsListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      dict_type_id: props.dictTypeId,
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delDictDetailsListApi(value)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '字典编号',
    show: false,
    disabled: false
  },
  {
    field: 'label',
    label: '字典标签',
    show: true,
    disabled: true
  },
  {
    field: 'value',
    label: '字典键值',
    show: true
  },
  {
    field: 'order',
    label: '字典排序',
    show: true
  },
  {
    field: 'disabled',
    label: '是否禁用',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch value={!row.disabled} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'remark',
    label: '备注',
    show: false
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: false
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
    field: 'label',
    label: '字典标签',
    component: 'Input',
    componentProps: {
      clearable: false
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
  const res = await getDictDetailsApi(row.id)
  if (res) {
    dialogTitle.value = '编辑字段元素'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增字段元素'
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
        res.value = await addDictDetailsListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putDictDetailsListApi(formData)
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

watch(
  () => props.dictTypeId,
  () => {
    getList()
  },
  {
    deep: true
  }
)
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      activeUID="detail"
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
            <ElButton type="primary" @click="addAction">新增字典元素</ElButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="650">
    <Write ref="writeRef" :current-row="currentRow" :dict-type-id="dictTypeId" />

    <template #footer>
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
