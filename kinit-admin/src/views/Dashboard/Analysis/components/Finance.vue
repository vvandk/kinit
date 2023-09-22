<script setup lang="ts">
import {
  ElRow,
  ElCol,
  ElDivider,
  ElSkeleton,
  ElTable,
  ElTableColumn,
  ElRadioGroup,
  ElRadioButton,
  ElDatePicker
} from 'element-plus'
import { formatMoney } from '@/utils'
import { ref, reactive } from 'vue'
import { Echart } from '@/components/Echart'
import { lineOptions, line2Options, pieOptions } from './finance-echarts-data'
import { EChartsOption } from 'echarts'

const loading = ref(false)

const lineOptionsData = reactive<EChartsOption>(lineOptions) as EChartsOption
const pieOptionsData = reactive<EChartsOption>(pieOptions) as EChartsOption

const tableData = ref([
  {
    name: '美的家用落地扇',
    category: '电风扇',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  },
  {
    name: '天斧88d 3u',
    category: '羽毛球拍',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  },
  {
    name: '格力空调',
    category: '空调',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  },
  {
    name: '海尔冰箱',
    category: '冰箱',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  },
  {
    name: '小米电视',
    category: '电视',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  },
  {
    name: '荣耀笔记本',
    category: '笔记本',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  },
  {
    name: 'iPhone12',
    category: '手机',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  },
  {
    name: 'Macbook Pro',
    category: '笔记本',
    order_quantity: '131',
    buy_user_number: '72',
    sales: '36981',
    sales_volume: '90'
  }
])

const radio = ref(0)
const date = ref()
const handleDateRadioChange = () => {}

const disabledDateFn = (time: any) => {
  return new Date('2023/01/01').getTime() > time.getTime() || time.getTime() > Date.now()
}
</script>

<template>
  <ElRadioGroup v-model="radio" @change="handleDateRadioChange">
    <ElRadioButton label="0">全部</ElRadioButton>
    <ElRadioButton label="1">今天</ElRadioButton>
    <ElRadioButton label="2">昨天</ElRadioButton>
    <ElRadioButton label="3">最近7天</ElRadioButton>
    <ElRadioButton label="4">最近30天</ElRadioButton>
    <ElDatePicker
      class="ml-2"
      v-model="date"
      type="daterange"
      range-separator="-"
      start-placeholder="开始时间"
      end-placeholder="结束时间"
      :disabled-date="disabledDateFn"
      :unlink-panels="true"
      size="default"
    />
  </ElRadioGroup>
  <ElDivider />
  <ElRow :gutter="20" class="pt-4">
    <ElCol :xs="12" :sm="6" class="border-r-1 border-r-[#f0f0f0] b-r-solid mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div>
          <div class="text-[#787a7d] text-[12px]">销售额</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">{{ formatMoney(899999.0) }}</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="12" :sm="6" class="border-r-1 border-r-[#f0f0f0] b-r-solid mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div>
          <div class="text-[#787a7d] text-[12px]">充值金额</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">{{ formatMoney(899999.0) }}</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="12" :sm="6" class="border-r-1 border-r-[#f0f0f0] b-r-solid mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div>
          <div class="text-[#787a7d] text-[12px]">销量</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">3999</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="12" :sm="6" class="border-r-1 border-r-[#f0f0f0] b-r-solid">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div>
          <div class="text-[#787a7d] text-[12px]">订单数</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">1899</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="12" :sm="6" />
  </ElRow>
  <ElDivider />
  <ElSkeleton :loading="loading" animated :rows="4">
    <Echart :options="line2Options" :height="350" />
  </ElSkeleton>
  <ElDivider />
  <ElRow :gutter="20" class="pt-4">
    <ElCol :xs="24" :sm="6">
      <ElSkeleton :loading="loading" animated :rows="4">
        <Echart :options="pieOptionsData" :height="350" />
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="18">
      <ElSkeleton :loading="loading" animated :rows="4">
        <Echart :options="lineOptionsData" :height="350" />
      </ElSkeleton>
    </ElCol>
  </ElRow>

  <ElDivider />

  <div class="mt-8">
    <ElTable
      :data="tableData"
      v-loading="loading"
      style="width: 100%"
      :headerCellStyle="{
        'background-color': '#f5f7fa',
        color: '#787a7d',
        'font-size': '12px'
      }"
    >
      <ElTableColumn type="index" width="50" />
      <ElTableColumn prop="name" label="商品名称" />
      <ElTableColumn prop="category" label="商品品类" />
      <ElTableColumn prop="order_quantity" label="商品购买次数" />
      <ElTableColumn prop="buy_user_number" label="商品购买人数" />
      <ElTableColumn prop="sales" label="商品销售额" align="center">
        <template #default="{ row }">
          <span>{{ formatMoney(row.sales) }}</span>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="sales_volume" label="商品销量" align="center" />
    </ElTable>
  </div>
</template>

<style scoped></style>
