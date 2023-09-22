<script setup lang="tsx">
import { PropType, reactive, ref } from 'vue'
import { Descriptions, DescriptionsSchema } from '@/components/Descriptions'
import { ElSwitch } from 'element-plus'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import { JsonViewer } from 'vue3-json-viewer'
import 'vue3-json-viewer/dist/index.css'

defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  }
})

const platformOptions = ref<DictDetail[]>([])
const loginMethodOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_platform', 'sys_vadmin_login_method'])
  platformOptions.value = dictOptions.sys_vadmin_platform
  loginMethodOptions.value = dictOptions.sys_vadmin_login_method
}

getOptions()

const detailSchema = reactive<DescriptionsSchema[]>([
  {
    field: 'id',
    label: '编号',
    minWidth: 100,
    span: 24
  },
  {
    field: 'telephone',
    label: '手机号',
    span: 24
  },
  {
    field: 'status',
    label: '登录状态',
    span: 24,
    slots: {
      default: (data: any) => {
        return (
          <>
            <ElSwitch value={data.status} size="small" disabled />
          </>
        )
      }
    }
  },
  {
    field: 'platform',
    label: '登录平台',
    span: 24,
    slots: {
      default: (data: any) => {
        return (
          <>
            <div>{selectDictLabel(platformOptions.value, data.platform)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'login_method',
    label: '认证方式',
    span: 24,
    slots: {
      default: (data: any) => {
        return (
          <>
            <div>{selectDictLabel(loginMethodOptions.value, data.login_method)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'ip',
    label: '登录地址',
    span: 24
  },
  {
    field: 'address',
    label: '登录地点',
    span: 24
  },
  {
    field: 'postal_code',
    label: '邮政编码',
    span: 24
  },
  {
    field: 'area_code',
    label: '地区区号',
    span: 24
  },
  {
    field: 'browser',
    label: '浏览器',
    span: 24
  },
  {
    field: 'system',
    label: '操作系统',
    span: 24
  },
  {
    field: 'response',
    label: '响应信息',
    span: 24,
    slots: {
      default: (data: any) => {
        return (
          <>
            <JsonViewer value={JSON.parse(data.request)} copyable boxed sort />
          </>
        )
      }
    }
  },
  {
    field: 'request',
    label: '请求信息',
    span: 24,
    slots: {
      default: (data: any) => {
        return (
          <>
            <JsonViewer value={JSON.parse(data.request)} copyable boxed sort />
          </>
        )
      }
    }
  },
  {
    field: 'create_datetime',
    label: '创建时间',
    span: 24
  }
])
</script>

<template>
  <Descriptions :schema="detailSchema" :data="currentRow || {}" />
</template>
