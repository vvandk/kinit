<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { addImagesApi, getImagesListApi, delImagesListApi } from '@/api/vadmin/resource/images'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElMessage, ElRow, ElCol, ElImage } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useClipboard } from '@vueuse/core'

defineOptions({
  name: 'ResourceImage'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getImagesListApi({
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
    const res = await delImagesListApi(value as number[])
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'selection',
    type: 'selection',
    show: true,
    disabled: true
  },
  {
    field: 'id',
    label: '编号',
    show: true,
    disabled: false,
    align: 'center',
    headerAlign: 'center',
    width: '80px'
  },
  {
    field: 'image_url',
    label: '图片',
    show: true,
    disabled: true,
    minWidth: '90px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div class="resource-image-name flex items-center">
              <div>
                <ElImage
                  src={`${row.image_url}?x-oss-process=image/resize,m_fixed,h_100`}
                  zoom-rate={1.2}
                  preview-src-list={dataList.value.map((item) => item.image_url)}
                  preview-teleported={true}
                  initial-index={data.$index}
                  style="height: 60px; display: block"
                  fit="cover"
                />
              </div>
              <div class="leading-[35px] ml-2 truncate">
                <span>{row.filename}</span>
              </div>
            </div>
          </>
        )
      }
    }
  },
  {
    field: 'remark',
    label: '备注',
    show: false,
    disabled: false
  },
  {
    field: 'update_datetime',
    label: '更新时间',
    show: false,
    width: '180px'
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    width: '180px',
    show: true
  },
  {
    field: 'create_user.name',
    label: '创建人',
    show: false
  },
  {
    field: 'action',
    width: '200px',
    label: '操作',
    fixed: 'right',
    disabled: false,
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => toCopy(row.id)}>
              复制编号
            </ElButton>
            <ElButton type="primary" link size="small" onClick={() => toCopy(row.image_url)}>
              复制链接
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
    field: 'filename',
    label: '文件名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
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

// 复制数据到剪切板
const toCopy = async (value: string) => {
  // 复制功能打包部署到线上后，需要线上地址使用 https 才可使用
  const { copy } = useClipboard()
  await copy(value)
  return ElMessage.success('复制成功')
}

const addAction = () => {
  dialogTitle.value = '新增图片素材'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    formData?.images.forEach((item) => (item.status = 'uploading'))
    if (formData?.upload_method === '2') {
      // 按顺序上传文件
      for (const item of formData?.images) {
        const data = new FormData()
        data.append('file', item.raw)
        await addImagesApi(data)
        item.status = 'success'
      }
    } else if (formData?.upload_method === '1') {
      // 同时上传文件
      const uploadPromises = formData?.images.map(async (item) => {
        const data = new FormData()
        data.append('file', item.raw)
        await addImagesApi(data)
        item.status = 'success'
      })
      await Promise.all(uploadPromises)
    }
    // 全部上传完成后执行的代码
    getList()
    dialogVisible.value = false
    saveLoading.value = false
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
            <ElButton type="primary" @click="addAction">新增图片素材</ElButton>
            <ElButton type="danger" @click="delData(null)">批量删除</ElButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" width="996px" height="600px" top="3vh">
    <Write ref="writeRef" :current-row="currentRow" />

    <template #footer>
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
