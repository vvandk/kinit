<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getIssueListApi, delIssueListApi } from '@/api/vadmin/help/issue'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { useDictStore } from '@/store/modules/dict'
import { DictDetail } from '@/utils/dict'
import { useRouter } from 'vue-router'

defineOptions({
  name: 'HelpIssue'
})

const { push } = useRouter()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getIssueListApi({
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
    const res = await delIssueListApi(value)
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
    disabled: true,
    width: '120px'
  },
  {
    field: 'category.name',
    label: '类别名称',
    width: '200px',
    show: true,
    disabled: true
  },
  {
    field: 'title',
    label: '标题',
    show: true
  },
  {
    field: 'view_number',
    label: '查看次数',
    show: true,
    width: '100px'
  },
  {
    field: 'is_active',
    label: '是否可见',
    show: true,
    width: '100px',
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
    width: '200px',
    sortable: true
  },
  {
    field: 'create_user.name',
    label: '创建人',
    show: true,
    width: '100px'
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
      options: platformOptions.value
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

const editAction = async (row: any) => {
  push(`/help/issue/form?id=${row.id}`)
}

const addAction = () => {
  push('/help/issue/form')
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
            <ElButton type="primary" @click="addAction">新增常见问题</ElButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>
</template>
