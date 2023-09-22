<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getRoleListApi,
  addRoleListApi,
  delRoleListApi,
  putRoleListApi,
  getRoleApi
} from '@/api/vadmin/auth/role'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'

defineOptions({
  name: 'AuthRole'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getRoleListApi({
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
    const res = await delRoleListApi(value)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '角色编号',
    show: true,
    disabled: true
  },
  {
    field: 'name',
    label: '角色名称',
    show: true,
    disabled: true
  },
  {
    field: 'role_key',
    label: '权限字符',
    show: true
  },
  {
    field: 'order',
    label: '显示顺序',
    show: true
  },
  {
    field: 'disabled',
    label: '角色状态',
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
    field: 'is_admin',
    label: '最高权限',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch value={!row.is_admin} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true
  },
  {
    field: 'action',
    width: '150px',
    label: '操作',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        const update = ['auth.role.update']
        const del = ['auth.role.delete']
        return (
          <>
            <ElButton
              v-show={row.id !== 1}
              type="primary"
              v-hasPermi={update}
              link
              size="small"
              onClick={() => editAction(row)}
            >
              编辑
            </ElButton>
            <ElButton
              v-show={row.id !== 1}
              type="danger"
              v-hasPermi={del}
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
    label: '角色名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'role_key',
    label: '权限字符',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'disabled',
    label: '状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '正常',
          value: false
        },
        {
          label: '停用',
          value: true
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
  const res = await getRoleApi(row.id)
  if (res) {
    dialogTitle.value = '编辑'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增'
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
        res.value = await addRoleListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putRoleListApi(formData)
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
            <ElButton type="primary" v-hasPermi="['auth.role.create']" @click="addAction"
              >新增角色</ElButton
            >
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
