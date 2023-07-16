<script lang="ts">
export default {
  name: 'AuthUser'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getUserListApi,
  addUserListApi,
  delUserListApi,
  putUserListApi,
  getUserApi,
  postExportUserQueryListApi
} from '@/api/vadmin/auth/user'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/user.data'
import { ref, unref, watch, nextTick } from 'vue'
import Write from './components/Write.vue'
import Import from './components/Import.vue'
import PasswordSendSMS from './components/PasswordSendSMS.vue'
import PasswordSendEmail from './components/PasswordSendEmail.vue'
import { Dialog } from '@/components/Dialog'
import {
  ElButton,
  ElMessage,
  ElSwitch,
  ElRow,
  ElCol,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem,
  ElIcon
} from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { RightToolbar } from '@/components/RightToolbar'
import { Search } from '@/components/Search'
import { useAppStore } from '@/store/modules/app'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'

const { wsCache } = useCache()
const appStore = useAppStore()

const { t } = useI18n()

const authStore = useAuthStoreWithOut()

const genderOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_gender'])
  genderOptions.value = dictOptions.sys_vadmin_gender
}

getOptions()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getUserListApi,
  delListApi: delUserListApi,
  exportQueryListApi: postExportUserQueryListApi,
  response: {
    data: 'data',
    count: 'count'
  },
  defaultParams: {
    is_active: true
  },
  props: {
    columns
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const actionType = ref('')
const loading = ref(false)

const { getList, setSearchParams, exportQueryList } = methods

// 添加事件
const addAction = () => {
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = async (row: any) => {
  const res = await getUserApi(row.id)
  if (res) {
    dialogTitle.value = '编辑'
    res.data.role_ids = res.data.roles.map((item: any) => item.id)
    tableObject.currentRow = res.data
    dialogVisible.value = true
    actionType.value = 'edit'
  }
}

// 删除事件
const delDatas = async (row: any) => {
  const { delListApi, getSelections } = methods
  const selections = ref([] as any[])
  if (row) {
    selections.value = [row.id]
  } else {
    selections.value = await getSelections()
    selections.value = selections.value.map((item) => item.id)
  }
  await delListApi(true, selections.value)
}

const writeRef = ref<ComponentRef<typeof Write>>()

const save = async () => {
  const write = unref(writeRef)
  await write?.elFormRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      let data = await write?.getFormData()
      if (!data) {
        loading.value = false
        return ElMessage.error('未获取到数据')
      }
      try {
        const res = ref({})
        if (actionType.value === 'add') {
          res.value = await addUserListApi(data)
          if (res.value) {
            dialogVisible.value = false
            getList()
          }
        } else if (actionType.value === 'edit') {
          const user = authStore.getUser
          const userId = data.id
          const userTelephone = data.telephone
          res.value = await putUserListApi(data)
          if (res.value) {
            dialogVisible.value = false
            if (user.id === userId && user.telephone !== userTelephone) {
              dialogVisible.value = false
              authStore.logout()
              return ElMessage.warning('认证已过期，请您重新登陆！')
            } else {
              getList()
            }
          }
        }
      } finally {
        loading.value = false
      }
    }
  })
}

getList()

const tableSize = ref('default')

watch(tableSize, (val) => {
  tableSize.value = val
})

const route = useRouter()
const cacheTableHeadersKey = route.currentRoute.value.fullPath

watch(
  columns,
  async (val) => {
    wsCache.set(cacheTableHeadersKey, JSON.stringify(val))
    await nextTick()
    elTableRef.value?.doLayout()
  },
  {
    deep: true
  }
)

const importDialogVisible = ref(false)
const importDialogTitle = ref('批量导入用户')

// 批量导入用户
const importList = () => {
  importDialogVisible.value = true
}

const passwordDialogVisible = ref(false)
let passwordDialogType = 'sms'
let passwordDialogTitle = ref('重置密码并发送短信')
const selections = ref([] as any[])

// 批量发送密码至短信
const sendPasswordToSMS = async () => {
  const { getSelections } = methods
  selections.value = await getSelections()
  if (selections.value.length > 0) {
    passwordDialogVisible.value = true
    passwordDialogType = 'sms'
    passwordDialogTitle.value = '重置密码并发送短信'
  } else {
    return ElMessage.warning('请先选择数据')
  }
}

// 批量发送密码至邮件
const sendPasswordToEmail = async () => {
  const { getSelections } = methods
  selections.value = await getSelections()
  if (selections.value.length > 0) {
    passwordDialogVisible.value = true
    passwordDialogType = 'email'
    passwordDialogTitle.value = '重置密码并发送邮件'
  } else {
    return ElMessage.warning('请先选择数据')
  }
}

const mobile = appStore.getMobile

// 下拉菜单处理事件
const handleCommand = (command: string) => {
  if (command === 'a') {
    importList()
  } else if (command === 'b') {
    exportQueryList()
  } else if (command === 'c') {
    sendPasswordToSMS()
  } else if (command === 'd') {
    sendPasswordToEmail()
  } else if (command === 'e') {
    delDatas(null)
  }
}
</script>

<template>
  <ContentWrap>
    <Search
      :model="{ is_active: true }"
      :schema="searchSchema"
      @search="setSearchParams"
      @reset="setSearchParams"
    />

    <div class="mb-8px flex justify-between">
      <ElRow :gutter="10">
        <ElCol :span="1.5" v-hasPermi="['auth.user.create']">
          <ElButton type="primary" @click="addAction">新增用户</ElButton>
        </ElCol>
        <ElCol :span="1.5" v-hasPermi="['auth.user.import']" v-if="!mobile">
          <ElButton @click="importList">批量导入用户</ElButton>
        </ElCol>
        <ElCol :span="1.5" v-hasPermi="['auth.user.export']" v-if="!mobile">
          <ElButton @click="exportQueryList">导出筛选用户</ElButton>
        </ElCol>
        <ElCol :span="1.5" v-hasPermi="['auth.user.reset']" v-if="!mobile">
          <ElButton @click="sendPasswordToSMS">重置密码通知短信</ElButton>
        </ElCol>
        <ElCol :span="1.5" v-hasPermi="['auth.user.reset']" v-if="!mobile">
          <ElButton @click="sendPasswordToEmail">重置密码通知邮件</ElButton>
        </ElCol>
        <ElCol :span="1.5" v-hasPermi="['auth.user.delete']" v-if="!mobile">
          <ElButton type="danger" @click="delDatas(null)">批量删除</ElButton>
        </ElCol>
        <ElCol :span="1.5" v-if="mobile">
          <ElDropdown trigger="click" @command="handleCommand">
            <ElButton>
              更多
              <el-icon class="el-icon--right">
                <Icon icon="mdi:keyboard-arrow-down" />
              </el-icon>
            </ElButton>
            <template #dropdown>
              <ElDropdownMenu>
                <ElDropdownItem command="a" v-hasPermi="['auth.user.import']"
                  >批量导入用户</ElDropdownItem
                >
                <ElDropdownItem command="b" v-hasPermi="['auth.user.export']"
                  >导出筛选用户</ElDropdownItem
                >
                <ElDropdownItem command="c" v-hasPermi="['auth.user.reset']"
                  >重置密码通知短信</ElDropdownItem
                >
                <ElDropdownItem command="d" v-hasPermi="['auth.user.reset']"
                  >重置密码通知邮件</ElDropdownItem
                >
                <ElDropdownItem command="e" v-hasPermi="['auth.user.delete']"
                  >批量删除</ElDropdownItem
                >
              </ElDropdownMenu>
            </template>
          </ElDropdown>
        </ElCol>
      </ElRow>
      <RightToolbar
        @get-list="getList"
        v-model:table-size="tableSize"
        v-model:columns="columns"
        :cache-table-headers-key="cacheTableHeadersKey"
      />
    </div>

    <Table
      v-model:limit="tableObject.limit"
      v-model:page="tableObject.page"
      :data="tableObject.tableData"
      :loading="tableObject.loading"
      :columns="columns"
      :selection="true"
      :size="tableSize"
      :border="true"
      :pagination="{
        total: tableObject.count
      }"
      @register="register"
    >
      <template #action="{ row }">
        <ElButton
          type="primary"
          v-hasPermi="['auth.user.update']"
          link
          size="small"
          @click="updateAction(row)"
        >
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton
          type="danger"
          v-hasPermi="['auth.user.delete']"
          link
          size="small"
          @click="delDatas(row)"
          v-if="authStore.getUser.id !== row.id && row.id !== 1"
        >
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>

      <template #is_active="{ row }">
        <ElSwitch :value="row.is_active" disabled />
      </template>

      <template #is_staff="{ row }">
        <ElSwitch :value="row.is_staff" disabled />
      </template>

      <template #gender="{ row }">
        {{ selectDictLabel(genderOptions, row.gender) }}
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

    <Dialog v-model="importDialogVisible" :title="importDialogTitle" width="750px" height="550px">
      <Import @get-list="getList" />
    </Dialog>

    <Dialog
      v-model="passwordDialogVisible"
      :title="passwordDialogTitle"
      width="1000px"
      height="550px"
    >
      <PasswordSendSMS
        v-if="passwordDialogType === 'sms'"
        :selections="selections"
        @get-list="getList"
      />

      <PasswordSendEmail
        v-else-if="passwordDialogType === 'email'"
        :selections="selections"
        @get-list="getList"
      />
    </Dialog>
  </ContentWrap>
</template>

<style scoped>
.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
