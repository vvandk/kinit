<script lang="ts">
export default {
  name: 'AuthMenu'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { RightToolbar } from '@/components/RightToolbar'
import { Table } from '@/components/Table'
import {
  getMenuListApi,
  delMenuListApi,
  addMenuListApi,
  putMenuListApi
} from '@/api/vadmin/auth/menu'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { ElButton, ElSwitch, ElRow, ElCol } from 'element-plus'
import { ref, unref, watch, nextTick } from 'vue'
import { Dialog } from '@/components/Dialog'
import Write from './components/Write.vue'
import { columns } from './components/menu.data'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'

const { wsCache } = useCache()
const { t } = useI18n()

let menuTypeOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_menu_type'])
  menuTypeOptions.value = dictOptions.sys_vadmin_menu_type
}

getOptions()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getMenuListApi,
  delListApi: delMenuListApi,
  response: {
    data: 'data'
  }
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const actionType = ref('')
const parentId = ref()

// 添加事件
const AddAction = () => {
  parentId.value = null
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 编辑事件
const updateAction = (row: any) => {
  parentId.value = null
  dialogTitle.value = '编辑'
  tableObject.currentRow = row
  dialogVisible.value = true
  actionType.value = 'edit'
}

// 删除事件
const delData = async (row: any) => {
  parentId.value = null
  const { delListApi } = methods
  await delListApi(true, [row.id])
}

// 添加子菜单事件
const addSonMenu = async (row: any) => {
  parentId.value = row.id
  dialogTitle.value = t('exampleDemo.add')
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

const loading = ref(false)

const writeRef = ref<ComponentRef<typeof Write>>()

const save = async () => {
  const write = unref(writeRef)
  await write?.elFormRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      const data = await write?.getFormData()
      try {
        const res = ref({})
        if (actionType.value === 'add') {
          res.value = await addMenuListApi(data)
          if (res.value) {
            dialogVisible.value = false
            getList()
          }
        } else if (actionType.value === 'edit') {
          res.value = await putMenuListApi(data)
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

const { getList } = methods

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
    <div class="mb-8px flex justify-between">
      <ElRow :gutter="10">
        <ElCol :span="1.5">
          <ElButton type="primary" v-hasPermi="['auth.menu.create']" @click="AddAction"
            >新增菜单</ElButton
          >
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
      :data="tableObject.tableData"
      :loading="tableObject.loading"
      :selection="false"
      :columns="columns"
      :border="true"
      :size="tableSize"
      row-key="id"
      default-expand-all
      @register="register"
    >
      <template #title="{ row }">
        {{ t(row.title) }}
      </template>
      <template #icon="{ row }">
        <div v-if="row.icon">
          <Icon :icon="row.icon" />
        </div>
      </template>
      <template #action="{ row }">
        <ElButton
          type="primary"
          v-hasPermi="['auth.menu.update']"
          link
          size="small"
          @click="updateAction(row)"
        >
          {{ t('exampleDemo.edit') }}
        </ElButton>
        <ElButton
          type="primary"
          v-hasPermi="['auth.menu.create']"
          link
          size="small"
          @click="addSonMenu(row)"
        >
          添加子菜单
        </ElButton>
        <ElButton
          type="danger"
          v-hasPermi="['auth.menu.delete']"
          link
          size="small"
          @click="delData(row)"
        >
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>

      <template #menu_type="{ row }">
        <span>
          {{ selectDictLabel(menuTypeOptions, row.menu_type) }}
        </span>
      </template>

      <template #hidden="{ row }">
        <ElSwitch :value="!row.hidden" disabled />
      </template>

      <template #noCache="{ row }">
        <ElSwitch :value="!row.noCache" disabled />
      </template>

      <template #disabled="{ row }">
        <ElSwitch :value="!row.disabled" disabled />
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <Write ref="writeRef" :current-row="tableObject.currentRow" :parent-id="parentId" />

      <template #footer>
        <ElButton type="primary" :loading="loading" @click="save">
          {{ t('exampleDemo.save') }}
        </ElButton>
        <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
      </template>
    </Dialog>
  </ContentWrap>
</template>
