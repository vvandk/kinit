<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getRecordLoginListApi } from '@/api/vadmin/system/record/login'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Detail from './components/Detail.vue'
import { Dialog } from '@/components/Dialog'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'

defineOptions({
  name: 'SystemRecordLogin'
})

const { t } = useI18n()

const platformOptions = ref<DictDetail[]>([])
const loginMethodOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_platform', 'sys_vadmin_login_method'])
  platformOptions.value = dictOptions.sys_vadmin_platform
  loginMethodOptions.value = dictOptions.sys_vadmin_login_method
}

getOptions()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getRecordLoginListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    show: true,
    disabled: true,
    width: '120px'
  },
  {
    field: 'telephone',
    label: '手机号',
    width: '150px',
    show: true,
    disabled: true
  },
  {
    field: 'status',
    label: '登录状态',
    show: true,
    slots: {
      default: (data: any) => {
        return (
          <>
            <ElSwitch value={data.row.status} size="small" disabled />
          </>
        )
      }
    }
  },
  {
    field: 'platform',
    label: '登录平台',
    width: '150px',
    show: true,
    slots: {
      default: (data: any) => {
        return (
          <>
            <div>{selectDictLabel(platformOptions.value, data.row.platform)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'login_method',
    label: '认证方式',
    width: '150px',
    show: true,
    slots: {
      default: (data: any) => {
        return (
          <>
            <div>{selectDictLabel(loginMethodOptions.value, data.row.login_method)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'ip',
    label: '登录地址',
    show: true,
    disabled: true,
    width: '150px'
  },
  {
    field: 'address',
    label: '登录地点',
    show: true
  },
  {
    field: 'postal_code',
    label: '邮政编码',
    show: false
  },
  {
    field: 'area_code',
    label: '地区区号',
    show: false
  },
  {
    field: 'browser',
    label: '浏览器',
    show: true
  },
  {
    field: 'system',
    label: '操作系统',
    show: true
  },
  {
    field: 'response',
    label: '响应信息',
    show: false,
    disabled: true
  },
  {
    field: 'request',
    label: '请求信息',
    show: false,
    disabled: true
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    show: true,
    sortable: true
  },
  {
    field: 'action',
    label: '操作',
    show: true,
    width: 100,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link onClick={() => action(row, 'detail')}>
              详情
            </ElButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'telephone',
    label: '手机号',
    component: 'Input',
    componentProps: {
      clearable: false,
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
    field: 'ip',
    label: '登录地址',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'address',
    label: '登录地点',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'status',
    label: '登录状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '登录成功',
          value: true
        },
        {
          label: '登录失败',
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

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const action = (row: any, type: string) => {
  dialogTitle.value = t('exampleDemo.detail')
  actionType.value = type
  currentRow.value = row
  dialogVisible.value = true
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
      node-key="id"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    />
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
    <Detail v-if="actionType === 'detail'" :current-row="currentRow" />

    <template #footer>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
