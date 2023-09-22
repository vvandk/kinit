<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getMenuListApi,
  delMenuListApi,
  addMenuListApi,
  putMenuListApi
} from '@/api/vadmin/auth/menu'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol } from 'element-plus'
import { Icon } from '@/components/Icon'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'

defineOptions({
  name: 'AuthMenu'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getMenuListApi({
      page: unref(currentPage),
      limit: unref(pageSize)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delMenuListApi(value)
    return res.code === 200
  }
})

const { dataList, loading } = tableState
const { getList, delList } = tableMethods

let menuTypeOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_menu_type'])
  menuTypeOptions.value = dictOptions.sys_vadmin_menu_type
}

getOptions()

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'title',
    label: '菜单名称',
    width: '200px',
    disabled: true,
    show: true
  },
  {
    field: 'icon',
    label: '图标',
    width: '120px',
    show: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return <>{row.icon ? <Icon icon={row.icon} /> : ''}</>
      }
    }
  },
  {
    field: 'order',
    label: '排序',
    width: '120px',
    show: true
  },
  {
    field: 'menu_type',
    label: '菜单类型',
    width: '120px',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <span>{selectDictLabel(menuTypeOptions.value, row.menu_type)}</span>
          </>
        )
      }
    }
  },
  {
    field: 'perms',
    label: '权限标识',
    width: '150px',
    show: true
  },
  {
    field: 'path',
    label: '路由地址',
    show: true
  },
  {
    field: 'component',
    label: '组件路径',
    show: true
  },
  {
    field: 'noCache',
    label: '页面缓存',
    width: '120px',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch value={!row.noCache} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'hidden',
    label: '显示状态',
    width: '120px',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch value={!row.hidden} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'disabled',
    label: '菜单状态',
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
    field: 'action',
    width: '200px',
    label: '操作',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        const update = ['auth.menu.update']
        const add = ['auth.menu.create']
        const del = ['auth.menu.delete']
        return (
          <>
            <ElButton
              type="primary"
              v-hasPermi={update}
              link
              size="small"
              onClick={() => editAction(row)}
            >
              编辑
            </ElButton>
            <ElButton
              type="primary"
              v-hasPermi={add}
              link
              size="small"
              onClick={() => addSonAction(row)}
            >
              添加子菜单
            </ElButton>
            <ElButton
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
  dialogTitle.value = '添加子菜单'
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
        res.value = await addMenuListApi(formData)
        if (res.value) {
          parentId.value = undefined
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putMenuListApi(formData)
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
            <ElButton type="primary" v-hasPermi="['auth.menu.create']" @click="addAction"
              >新增菜单</ElButton
            >
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle">
    <Write ref="writeRef" :current-row="currentRow" :parent-id="parentId" />

    <template #footer>
      <ElButton v-if="actionType !== 'detail'" type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
