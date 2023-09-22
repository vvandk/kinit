<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getUserListApi,
  addUserListApi,
  delUserListApi,
  putUserListApi,
  getUserApi,
  postExportUserQueryListApi
} from '@/api/vadmin/auth/user'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol, ElMessage } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import Import from './components/Import.vue'
import PasswordSendSMS from './components/PasswordSendSMS.vue'
import PasswordSendEmail from './components/PasswordSendEmail.vue'

defineOptions({
  name: 'AuthUser'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getUserListApi({
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
    const res = await delUserListApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await postExportUserQueryListApi(
      {
        page: unref(currentPage),
        limit: unref(pageSize),
        ...unref(searchParams)
      },
      headers
    )
    return res
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList, getSelections, exportQueryList } = tableMethods

const genderOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_gender'])
  genderOptions.value = dictOptions.sys_vadmin_gender
}

getOptions()

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'selection',
    type: 'selection',
    show: true,
    disabled: true
  },
  {
    field: 'id',
    label: '用户编号',
    width: '100px',
    show: true,
    disabled: true
  },
  {
    field: 'name',
    label: '姓名',
    show: true,
    disabled: true
  },
  {
    field: 'nickname',
    label: '昵称',
    show: true
  },
  {
    field: 'telephone',
    label: '手机号',
    show: true,
    disabled: true
  },
  {
    field: 'email',
    label: '邮箱',
    show: true,
    disabled: true
  },
  {
    field: 'gender',
    label: '性别',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>{selectDictLabel(unref(genderOptions), row.gender)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'roles',
    label: '角色',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div class="text-truncate">{row.roles.map((item) => item.name).join()}</div>
          </>
        )
      }
    }
  },
  {
    field: 'is_active',
    label: '是否可用',
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
    field: 'is_staff',
    label: '工作人员',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch value={row.is_staff} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'last_login',
    label: '最近登录时间',
    show: true,
    width: '190px'
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    width: '190px',
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
        const update = ['auth.user.update']
        const del = ['auth.user.delete']
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
    label: '姓名',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    },
    formItemProps: {
      labelWidth: '47px'
    }
  },
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
    field: 'is_active',
    label: '状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '正常',
          value: true
        },
        {
          label: '停用',
          value: false
        }
      ]
    }
  },
  {
    field: 'is_staff',
    label: '工作人员',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '是',
          value: true
        },
        {
          label: '否',
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

const delData = async (row?: any) => {
  delLoading.value = true
  if (row) {
    await delList(true, [row.id]).finally(() => {
      delLoading.value = false
    })
  } else {
    await delList(true).finally(() => {
      delLoading.value = false
    })
  }
}

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

const editAction = async (row: any) => {
  const res = await getUserApi(row.id)
  if (res) {
    dialogTitle.value = '编辑用户'
    res.data.role_ids = res.data.roles.map((item: any) => item.id)
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增用户'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

// 批量导入用户
const importList = () => {
  dialogTitle.value = '批量导入用户'
  actionType.value = 'import'
  currentRow.value = undefined
  dialogVisible.value = true
}

const selections = ref([] as any[])

// 批量发送密码至短信
const sendPasswordToSMS = async () => {
  selections.value = await getSelections()
  if (selections.value.length > 0) {
    dialogTitle.value = '重置密码并发送短信'
    actionType.value = 'sms'
    currentRow.value = undefined
    dialogVisible.value = true
  } else {
    return ElMessage.warning('请先选择数据')
  }
}

// 批量发送密码至邮件
const sendPasswordToEmail = async () => {
  selections.value = await getSelections()
  if (selections.value.length > 0) {
    dialogTitle.value = '重置密码并发送邮件'
    actionType.value = 'email'
    currentRow.value = undefined
    dialogVisible.value = true
  } else {
    return ElMessage.warning('请先选择数据')
  }
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addUserListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await putUserListApi(formData)
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
          <ElCol :span="1.5" v-hasPermi="['auth.user.create']">
            <ElButton type="primary" @click="addAction">新增用户</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['auth.user.import']">
            <ElButton @click="importList">批量导入用户</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['auth.user.export']">
            <ElButton @click="exportQueryList()">导出筛选用户</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['auth.user.reset']">
            <ElButton @click="sendPasswordToSMS">重置密码通知短信</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['auth.user.reset']">
            <ElButton @click="sendPasswordToEmail">重置密码通知邮件</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['auth.user.delete']">
            <ElButton type="danger" @click="delData(null)">批量删除</ElButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    :height="600"
    :width="actionType === 'sms' || actionType === 'email' ? '1000px' : '700px'"
  >
    <Write
      v-if="actionType === 'add' || actionType === 'edit'"
      ref="writeRef"
      :current-row="currentRow"
    />

    <Import v-else-if="actionType === 'import'" @get-list="getList" />

    <PasswordSendSMS
      v-else-if="actionType === 'sms'"
      :selections="selections"
      @get-list="getList"
    />

    <PasswordSendEmail
      v-else-if="actionType === 'email'"
      :selections="selections"
      @get-list="getList"
    />

    <template #footer v-if="actionType === 'add' || actionType === 'edit'">
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
