<script setup lang="ts">
import {
  ElLink,
  ElRow,
  ElCol,
  ElButton,
  ElTable,
  ElTableColumn,
  ElUpload,
  ElTooltip,
  UploadProps,
  ElMessage,
  ElPopconfirm
} from 'element-plus'
import { getImportTemplateApi, postImportUserApi } from '@/api/vadmin/auth/user'
import { ref } from 'vue'

const emit = defineEmits(['getList'])

const beforeFileUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const isExcel = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'].includes(
    rawFile.type
  )
  const isLtSize = rawFile.size / 1024 / 1024 < 10

  if (!isExcel) {
    ElMessage.error('上传文件必须是 XLSX 格式!')
  }
  if (!isLtSize) {
    ElMessage.error('上传文件大小不能超过 10MB!')
  }
  return isExcel && isLtSize
}

const importFile = ref()
const tableData = ref([] as Recordable[])
const resultTableData = ref([] as Recordable[])

const handleUpload = async (file) => {
  tableData.value = []
  tableData.value.push({
    filename: file.file.name,
    filesize: (file.file.size / 1024).toFixed(1) + 'KB',
    status: '上传成功'
  })
  importFile.value = file.file
}

const handleDelete = () => {
  tableData.value = []
  importFile.value = null
}

const importLoading = ref(false)
const successTotalNumber = ref(0)

const handleImport = async () => {
  importLoading.value = true
  const formData = new FormData()
  formData.append('file', importFile.value)
  try {
    const res = await postImportUserApi(formData)
    if (res) {
      resultTableData.value.push({
        filename: importFile.value.name,
        success_number: res.data.success_number,
        error_number: res.data.error_number,
        error_url: res.data.error_url
      })
      successTotalNumber.value += res.data.success_number
      handleDelete()
      emit('getList')
    }
  } finally {
    importLoading.value = false
  }
}

const downloadTemplate = async () => {
  ElMessage.info('正在下载请稍等！')
  const res = await getImportTemplateApi()
  if (res) {
    const a = document.createElement('a')
    a.style.display = 'none'
    a.href = res.data.url
    a.target = '_blank'
    a.download = res.data.filename
    const event = new MouseEvent('click')
    a.dispatchEvent(event)
  }
}

const downloadErrorFile = async (row: Recordable) => {
  ElMessage.info('正在下载请稍等！')
  const a = document.createElement('a')
  a.style.display = 'none'
  a.href = row.error_url
  a.target = '_blank'
  a.download = row.filename
  const event = new MouseEvent('click')
  a.dispatchEvent(event)
}
</script>

<template>
  <div>
    <span>导入步骤：</span>
    <ol>
      <li style="margin-top: 7px">
        <ElLink @click="downloadTemplate" target="_blank" type="primary">
          下载最新批量导入模板
        </ElLink>
      </li>
      <li style="margin-top: 7px">编辑模板文件，（将需要导入的数据按格式填写进去）</li>
      <li style="margin-top: 7px">上传模板文件，点击确认导入</li>
      <li style="margin-top: 7px">查看导入结果，是否全部导入</li>
    </ol>
  </div>
  <div>
    <ElRow :gutter="10" class="!mt-0 !mr-0">
      <ElCol :span="1.5">
        <div>
          <ElUpload
            action=""
            :http-request="handleUpload"
            :data="{ path: 'users' }"
            :show-file-list="false"
            :before-upload="beforeFileUpload"
            accept=".xlsx"
            :disabled="tableData.length > 0"
          >
            <ElTooltip effect="dark" content="只支持上传XLSX文件" placement="top">
              <ElButton type="primary" size="small" :disabled="tableData.length > 0"
                >上传文件</ElButton
              >
            </ElTooltip>
          </ElUpload>
        </div>
      </ElCol>
      <ElCol :span="1.5">
        <ElButton
          type="primary"
          size="small"
          :disabled="tableData.length === 0"
          :loading="importLoading"
          @click="handleImport"
          >确认导入</ElButton
        >
      </ElCol>
    </ElRow>
    <ElTable :data="tableData" :border="true" style="width: 100%" class="mt-10px">
      <ElTableColumn prop="filename" label="文件名称" align="left" />
      <ElTableColumn prop="filesize" label="文件大小" width="100" align="center" />
      <ElTableColumn prop="status" label="上传状态" width="100" align="center" />
      <ElTableColumn fixed="right" label="操作" width="130" align="center">
        <template #default>
          <ElPopconfirm title="确认删除吗?" @confirm="handleDelete">
            <template #reference>
              <ElButton link type="primary" size="small">删除</ElButton>
            </template>
          </ElPopconfirm>
        </template>
      </ElTableColumn>
    </ElTable>
  </div>
  <div class="mt-10px">
    <div class="flex justify-between mr-10px">
      <span>导入结果</span>
      <span>成功导入总数：{{ successTotalNumber }}</span>
    </div>
    <ElTable :data="resultTableData" :border="true" style="width: 100%" class="mt-10px">
      <ElTableColumn prop="filename" label="文件名称" align="left" />
      <ElTableColumn prop="success_number" label="成功数量" width="100" align="center" />
      <ElTableColumn prop="error_number" label="失败数量" width="100" align="center">
        <template #default="scope">
          <span style="color: red">{{ scope.row.error_number }}</span>
        </template>
      </ElTableColumn>
      <ElTableColumn fixed="right" label="操作" width="130" align="center">
        <template #default="scope">
          <ElLink
            v-if="scope.row.error_number > 0"
            @click="downloadErrorFile(scope.row)"
            target="_blank"
            type="primary"
            >下载失败数据</ElLink
          >
          <ElLink v-else type="success" :underline="false">成功全部导入</ElLink>
        </template>
      </ElTableColumn>
    </ElTable>
  </div>
</template>
