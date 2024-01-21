<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getDeptListApi,
  delDeptListApi,
  addDeptListApi,
  putDeptListApi
} from '@/api/vadmin/auth/dept'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch, ElRow, ElCol } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { BaseButton } from '@/components/Button'

defineOptions({
  name: 'AuthDept'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getDeptListApi({
      page: unref(currentPage),
      limit: unref(pageSize)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delDeptListApi(value)
    return res.code === 200
  }
})

const { dataList, loading } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'name',
    label: '部门名称',
    disabled: true,
    show: true
  },
  {
    field: 'dept_key',
    label: '部门标识',
    show: true
  },
  {
    field: 'owner',
    label: '负责人',
    show: true
  },
  {
    field: 'phone',
    label: '联系电话',
    show: true
  },
  {
    field: 'email',
    label: '邮箱',
    show: true
  },
  {
    field: 'desc',
    label: '描述',
    show: true
  },
  {
    field: 'order',
    label: '排序',
    width: '120px',
    show: true
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
            <ElSwitch modelValue={!row.disabled} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'action',
    width: '200px',
    label: '操作',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <BaseButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
            </BaseButton>
            <BaseButton type="primary" link size="small" onClick={() => addSonAction(row)}>
              添加子部门
            </BaseButton>
            <BaseButton
              type="danger"
              loading={delLoading.value}
              link
              size="small"
              onClick={() => delData(row)}
            >
              删除
            </BaseButton>
          </>
        )
      }
    }
  }
])

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
const parentId = ref(undefined)
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

const editAction = (row: any) => {
  dialogTitle.value = '编辑'
  actionType.value = 'edit'
  currentRow.value = row
  dialogVisible.value = true
}

const addAction = () => {
  dialogTitle.value = '新增'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const addSonAction = (row: any) => {
  dialogTitle.value = '添加子部门'
  actionType.value = 'addSon'
  parentId.value = row.id
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
      if (actionType.value === 'add' || actionType.value === 'addSon') {
        res.value = await addDeptListApi(formData)
        if (res.value) {
          parentId.value = undefined
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putDeptListApi(formData)
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
    <Table
      :columns="tableColumns"
      showAction
      default-expand-all
      node-key="id"
      :data="dataList"
      :loading="loading"
      @register="tableRegister"
      @refresh="getList"
    >
      <template #toolbar>
        <ElRow :gutter="10">
          <ElCol :span="1.5">
            <BaseButton type="primary" @click="addAction">新增部门</BaseButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle">
    <Write ref="writeRef" :current-row="currentRow" :parent-id="parentId" />

    <template #footer>
      <BaseButton
        v-if="actionType !== 'detail'"
        type="primary"
        :loading="saveLoading"
        @click="save"
      >
        {{ t('exampleDemo.save') }}
      </BaseButton>
      <BaseButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</BaseButton>
    </template>
  </Dialog>
</template>
