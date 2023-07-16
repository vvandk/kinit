<script lang="ts">
export default {
  name: 'AuthRole'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import {
  getRoleListApi,
  addRoleListApi,
  delRoleListApi,
  putRoleListApi,
  getRoleApi
} from '@/api/vadmin/auth/role'
import { useTable } from '@/hooks/web/useTable'
import { ElButton, ElMessage, ElSwitch, ElRow, ElCol } from 'element-plus'
import { columns, searchSchema } from './components/role.data'
import { ref, unref, watch, nextTick } from 'vue'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useI18n } from '@/hooks/web/useI18n'
import { RightToolbar } from '@/components/RightToolbar'
import { Search } from '@/components/Search'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'

const { wsCache } = useCache()
const { t } = useI18n()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getRoleListApi,
  delListApi: delRoleListApi,
  response: {
    data: 'data',
    count: 'count'
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const actionType = ref('')
const loading = ref(false)
const defaultCheckedKeys = ref([])

// 添加事件
const addAction = () => {
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
  defaultCheckedKeys.value = []
}

// 编辑事件
const updateAction = async (row: any) => {
  const res = await getRoleApi(row.id)
  if (res) {
    dialogTitle.value = '编辑'
    tableObject.currentRow = res.data
    defaultCheckedKeys.value = res.data.menus.map((item: any) => item.id)
    dialogVisible.value = true
    actionType.value = 'edit'
  }
}

// 删除事件
const delData = async (row: any) => {
  const { delListApi } = methods
  await delListApi(true, [row.id])
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
      data.menu_ids = write?.getTreeCheckedKeys()
      try {
        const res = ref({})
        if (actionType.value === 'add') {
          res.value = await addRoleListApi(data)
          if (res.value) {
            dialogVisible.value = false
            getList()
          }
        } else if (actionType.value === 'edit') {
          res.value = await putRoleListApi(data)
          if (res.value) {
            dialogVisible.value = false
            getList()
          }
        }
      } finally {
        loading.value = false
      }
    }
  })
}

const { getList, setSearchParams } = methods

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
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @search="setSearchParams" @reset="setSearchParams" />

    <div class="mb-8px flex justify-between">
      <ElRow :gutter="10">
        <ElCol :span="1.5" v-hasPermi="['auth.role.create']">
          <ElButton type="primary" @click="addAction">新增角色</ElButton>
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
      :size="tableSize"
      :border="true"
      :selection="false"
      :pagination="{
        total: tableObject.count
      }"
      @register="register"
    >
      <template #action="{ row }">
        <ElButton
          type="primary"
          v-hasPermi="['auth.role.update']"
          link
          size="small"
          @click="updateAction(row)"
          v-if="row.id !== 1"
        >
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton
          type="danger"
          v-hasPermi="['auth.role.delete']"
          link
          size="small"
          @click="delData(row)"
          v-if="row.id !== 1"
        >
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>

      <template #disabled="{ row }">
        <ElSwitch :value="!row.disabled" disabled />
      </template>

      <template #is_admin="{ row }">
        <ElSwitch :value="row.is_admin" disabled />
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="700px" height="600px">
      <Write
        ref="writeRef"
        :current-row="tableObject.currentRow"
        :default-checked-keys="defaultCheckedKeys"
      />

      <template #footer>
        <ElButton type="primary" :loading="loading" @click="save">
          {{ t('exampleDemo.save') }}
        </ElButton>
        <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
      </template>
    </Dialog>
  </ContentWrap>
</template>
