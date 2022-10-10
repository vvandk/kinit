<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getUserListApi,
  addUserListApi,
  delUserListApi,
  putUserListApi,
  getUserApi
} from '@/api/vadmin/auth/user'
import { useTable } from '@/hooks/web/useTable'
import { columns } from './components/user.data'
import { ref, unref } from 'vue'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { ElButton, ElMessage, ElSwitch } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { useRouter } from 'vue-router'

const { t } = useI18n()

const { replace } = useRouter()

const authStore = useAuthStoreWithOut()

let genderOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_gender'])
  genderOptions.value = dictOptions.sys_vadmin_gender
}

getOptions()

const { register, tableObject, methods } = useTable({
  getListApi: getUserListApi,
  delListApi: delUserListApi,
  response: {
    data: 'data',
    count: 'count'
  },
  props: {
    columns
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const actionType = ref('')
const loading = ref(false)

// 添加事件
const AddAction = () => {
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = async (row: any) => {
  const res = await getUserApi(row.id)
  dialogTitle.value = '编辑'
  res.data.role_ids = res.data.roles.map((item: any) => item.id)
  tableObject.currentRow = res.data
  dialogVisible.value = true
  actionType.value = 'edit'
}

// 删除事件
const delData = async (row: any) => {
  tableObject.currentRow = row
  const { delListApi } = methods
  loading.value = true
  await delListApi([row.id], false).finally(() => {
    loading.value = false
  })
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
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addUserListApi(data)
      } else if (actionType.value === 'edit') {
        const user = authStore.getUser
        res.value = await putUserListApi(data)
        if (user.id === data.id && user.telephone !== data.telephone) {
          dialogVisible.value = false
          authStore.logout()
          replace('/login')
          return ElMessage.warning('认证已过期，请您重新登陆！')
        }
      }
      if (res.value) {
        dialogVisible.value = false
        getList()
      }
      loading.value = false
    }
  })
}

const { getList } = methods

getList()
</script>

<template>
  <ContentWrap>
    <div class="mb-10px">
      <ElButton type="primary" @click="AddAction">{{ t('exampleDemo.add') }}</ElButton>
    </div>

    <Table
      v-model:limit="tableObject.limit"
      v-model:page="tableObject.page"
      :data="tableObject.tableData"
      :loading="tableObject.loading"
      :selection="false"
      :pagination="{
        total: tableObject.count
      }"
      @register="register"
    >
      <template #action="{ row }">
        <ElButton type="primary" text size="small" @click="updateAction(row)">
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton type="danger" text size="small" @click="delData(row)">
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>

      <template #is_active="{ row }">
        <ElSwitch :value="row.is_active" disabled />
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
  </ContentWrap>
</template>
