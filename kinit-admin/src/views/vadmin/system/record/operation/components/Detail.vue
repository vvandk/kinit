<script setup lang="tsx">
import { PropType, reactive } from 'vue'
import { Descriptions, DescriptionsSchema } from '@/components/Descriptions'

defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  }
})

const detailSchema = reactive<DescriptionsSchema[]>([
  {
    field: 'user_id',
    label: '操作人编号',
    width: '100px',
    span: 24
  },
  {
    field: 'user_name',
    label: '操作人',
    width: '100px',
    span: 24
  },
  {
    field: 'telephone',
    label: '手机号',
    width: '130px',
    span: 24
  },
  {
    field: 'request_method',
    label: '请求方法',
    width: '100px',
    span: 24
  },
  {
    field: 'client_ip',
    label: '客户端地址',
    width: '130px',
    span: 24
  },
  {
    field: 'tags',
    label: '标签',
    width: '130px',
    span: 24
  },
  {
    field: 'summary',
    label: '操作内容',
    span: 24
  },
  {
    field: 'description',
    label: '描述',
    span: 24
  },
  {
    field: 'status_code',
    label: '操作状态',
    width: '100px',
    span: 24
  },
  {
    field: 'route_name',
    label: '接口函数',
    width: '150px',
    span: 24
  },
  {
    field: 'api_path',
    label: '接口地址',
    span: 24
  },
  {
    field: 'params',
    label: '请求参数',
    span: 24
  },
  {
    field: 'browser',
    label: '浏览器',
    width: '150px',
    span: 24
  },
  {
    field: 'system',
    label: '系统',
    width: '150px',
    span: 24
  },
  {
    field: 'process_time',
    label: '总耗时',
    span: 24
  },
  {
    field: 'create_datetime',
    label: '操作时间',

    span: 24
  }
])
</script>

<template>
  <Descriptions :schema="detailSchema" :data="currentRow || {}" />
</template>
