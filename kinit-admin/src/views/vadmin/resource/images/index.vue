<script lang="ts">
export default {
  name: 'ResourceImages'
}
</script>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { addImagesApi, getImagesListApi, delImagesListApi } from '@/api/vadmin/resource/images'
import { useTable } from '@/hooks/web/useTable'
import { columns, searchSchema } from './components/images.data'
import { ref, watch, nextTick, unref } from 'vue'
import { ElRow, ElButton, ElCol, ElImage, ElMessage } from 'element-plus'
import { RightToolbar } from '@/components/RightToolbar'
import { useCache } from '@/hooks/web/useCache'
import { useRouter } from 'vue-router'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useI18n } from '@/hooks/web/useI18n'
import { Search } from '@/components/Search'
import { useClipboard } from '@vueuse/core'

const { wsCache } = useCache()
const { t } = useI18n()

const { register, elTableRef, tableObject, methods } = useTable({
  getListApi: getImagesListApi,
  delListApi: delImagesListApi,
  response: {
    data: 'data',
    count: 'count'
  }
})

const { getList, setSearchParams } = methods

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

const dialogVisible = ref(false)
const dialogTitle = ref('')
const loading = ref(false)
const actionType = ref('')

// 新增事件
const addAction = async () => {
  dialogTitle.value = '新增图片素材'
  tableObject.currentRow = null
  dialogVisible.value = true
  actionType.value = 'add'
}

// 删除事件
const delAction = async (row: any) => {
  const { delListApi } = methods
  if (row) {
    await delListApi(true, [row.id])
  } else {
    await delListApi(true)
  }
}

const writeRef = ref<ComponentRef<typeof Write>>()

// 提交事件
const save = async () => {
  const write = unref(writeRef)
  await write?.elFormRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      let data = await write?.getFormData()
      data?.images.forEach((item) => (item.status = 'uploading'))
      if (data?.upload_method === '2') {
        // 按顺序上传文件
        for (const item of data?.images) {
          const formData = new FormData()
          formData.append('file', item.raw)
          await addImagesApi(formData)
          item.status = 'success'
        }
      } else if (data?.upload_method === '1') {
        // 同时上传文件
        const uploadPromises = data?.images.map(async (item) => {
          const formData = new FormData()
          formData.append('file', item.raw)
          await addImagesApi(formData)
          item.status = 'success'
        })
        await Promise.all(uploadPromises)
      }
      // 全部上传完成后执行的代码
      getList()
      dialogVisible.value = false
      loading.value = false
    }
  })
}

// 复制数据到剪切板
const toCopy = async (value: string) => {
  // 复制功能打包部署到线上后，需要线上地址使用 https 才可使用
  const { copy } = useClipboard()
  await copy(value)
  return ElMessage.success('复制成功')
}

getList()
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @search="setSearchParams" @reset="setSearchParams" />

    <div class="mb-8px flex justify-between">
      <ElRow :gutter="10">
        <ElCol :span="1.5" v-shop>
          <ElButton type="primary" @click="addAction">新增图片素材</ElButton>
        </ElCol>
        <ElCol :span="1.5" v-shop>
          <ElButton type="danger" @click="delAction(null)">批量删除选中的图片素材</ElButton>
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
      :columns="columns"
      :data="tableObject.tableData"
      :loading="tableObject.loading"
      :selection="true"
      :size="tableSize"
      :border="true"
      :pagination="{
        total: tableObject.count
      }"
      @register="register"
    >
      <template #image_url="{ row, $index }">
        <div class="resource-image-name flex items-center">
          <div>
            <ElImage
              :src="`${row.image_url}?x-oss-process=image/resize,m_fixed,h_100`"
              :zoom-rate="1.2"
              :preview-src-list="tableObject.tableData.map((item) => item.image_url)"
              :preview-teleported="true"
              :initial-index="$index"
              style="height: 60px; display: block"
              fit="cover"
            />
          </div>
          <div class="leading-[35px] ml-2 truncate">
            <span>{{ row.filename }}</span>
          </div>
        </div>
      </template>

      <template #action="{ row }">
        <ElButton type="primary" link size="small" @click="toCopy(row.id)"> 复制图片编号 </ElButton>
        <ElButton type="primary" link size="small" @click="toCopy(row.image_url)">
          复制图片链接
        </ElButton>
        <ElButton v-shop type="danger" link size="small" @click="delAction(row)">
          {{ t('exampleDemo.del') }}
        </ElButton>
      </template>
    </Table>

    <Dialog v-model="dialogVisible" :title="dialogTitle" width="996px" height="600px" top="3vh">
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

<style lang="less">
.resource-image .image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 35px;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
</style>
