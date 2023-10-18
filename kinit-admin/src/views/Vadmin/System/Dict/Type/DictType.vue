<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getDictTypeListApi,
  addDictTypeListApi,
  delDictTypeListApi,
  putDictTypeListApi,
  getDictTypeApi
} from '@/api/vadmin/system/dict'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElMessage, ElSwitch, ElRow, ElCol } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { Icon } from '@/components/Icon'
import { useClipboard } from '@vueuse/core'

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getDictTypeListApi({
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
    const res = await delDictTypeListApi(value)
    if (res.code === 200) {
      await clearCurrentRow()
    }
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList, getElTableExpose } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '字典编号',
    width: '80px',
    show: false,
    disabled: false
  },
  {
    field: 'dict_name',
    label: '字典名称',
    show: true,
    disabled: true
  },
  {
    field: 'dict_type',
    label: '字典类型',
    show: true,
    disabled: true,
    slots: {
      default: (data: any) => {
        // 复制字典类型
        const toCopy = async (value: string) => {
          // 复制功能打包部署到线上后，需要线上地址使用 https 才可使用
          const { copy } = useClipboard()
          await copy(value)
          return ElMessage.success('复制成功')
        }

        const row = data.row
        return (
          <>
            <span onClick={() => toCopy(row.dict_type)}>
              <Icon icon="material-symbols:content-copy-rounded" class="cursor-pointer" />
            </span>
            <span>{row.dict_type}</span>
          </>
        )
      }
    }
  },
  {
    field: 'disabled',
    label: '是否禁用',
    width: '120px',
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
    field: 'dict_name',
    label: '字典名称',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      clearable: false
    }
  },
  {
    field: 'dict_type',
    label: '字典类型',
    colProps: {
      span: 24
    },
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
  const res = await getDictTypeApi(row.id)
  if (res) {
    dialogTitle.value = '编辑字典类型'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增字典类型'
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
        res.value = await addDictTypeListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putDictTypeListApi(formData)
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

const emit = defineEmits(['updateDictTypeId'])

const handleCurrentChange = async (val: any | undefined) => {
  emit('updateDictTypeId', val ? val.id : val)
}

const clearCurrentRow = async () => {
  const elTableExpost = await getElTableExpose()
  elTableExpost?.setCurrentRow(null)
  emit('updateDictTypeId', null)
}
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      activeUID="type"
      :columns="tableColumns"
      default-expand-all
      :highlightCurrentRow="true"
      node-key="id"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @current-change="handleCurrentChange"
      @refresh="getList"
    >
      <template #toolbar>
        <ElRow :gutter="10">
          <ElCol :span="1.5">
            <ElButton type="primary" @click="addAction">新增字典类型</ElButton>
          </ElCol>
          <ElCol :span="1.5">
            <ElButton type="danger" @click="clearCurrentRow">清除选择</ElButton>
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
