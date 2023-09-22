<script setup lang="ts">
import { ElRow, ElCol, ElSkeleton, ElRadioGroup, ElRadioButton, ElDatePicker } from 'element-plus'
import { ref, reactive } from 'vue'
import { Echart } from '@/components/Echart'
import {
  paySuccesslineOptions,
  newCustomerlineOptions,
  memberPieOptions,
  customerConversionLineOptions
} from './user-echarts-data'
import { EChartsOption } from 'echarts'
import { getRandomNumberApi } from '@/api/dashboard/analysis/index'

const loading = ref(false)

const newCustomerlineOptionsData = reactive<EChartsOption>(newCustomerlineOptions) as EChartsOption
const paySuccesslineOptionsData = reactive<EChartsOption>(paySuccesslineOptions) as EChartsOption
const customerConversionLineOptionsData = reactive<EChartsOption>(
  customerConversionLineOptions
) as EChartsOption
const pieOptionsData = reactive<EChartsOption>(memberPieOptions) as EChartsOption

const radio = ref(0)
const date = ref()
const handleDateRadioChange = () => {}

const disabledDateFn = (time: any) => {
  return new Date('2023/01/01').getTime() > time.getTime() || time.getTime() > Date.now()
}

const potentialNumber = ref(0)
const customerNumber = ref(0)
const memberNumber = ref(0)
const paySuccessCustomerNumber = ref(0)

// 获取潜客数
const getPotentialTotalNumber = async () => {
  const res = await getRandomNumberApi()
  if (res) {
    potentialNumber.value = res.data
  }
}

// 获取客户数
const getCustomerTotalNumber = async () => {
  const res = await getRandomNumberApi()
  if (res) {
    customerNumber.value = res.data
  }
}

// 获取会员数
const getMemberTotalNumber = async () => {
  const res = await getRandomNumberApi()
  if (res) {
    memberNumber.value = res.data
  }
}

// 获取支付成功客户数
const getPaySuccessCustomerTotalNumber = async () => {
  const res = await getRandomNumberApi()
  if (res) {
    paySuccessCustomerNumber.value = res.data
  }
}

const getAllApi = async () => {
  loading.value = true
  await Promise.all([
    getPotentialTotalNumber(),
    getCustomerTotalNumber(),
    getMemberTotalNumber(),
    getPaySuccessCustomerTotalNumber()
  ])
  loading.value = false
}

getAllApi()
</script>

<template>
  <div>
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
  </div>
  <ElRow :gutter="20" class="pt-4">
    <ElCol :xs="24" :sm="6" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#787a7d] text-[12px]">新增潜客数</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">{{ potentialNumber }}</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="6" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#787a7d] text-[12px]">新增客户数</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">{{ customerNumber }}</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="6" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#787a7d] text-[12px]">新增会员数</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">{{ memberNumber }}</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="6" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#787a7d] text-[12px]">支付成功客户数</div>
          <div class="text-[#121315] text-[20px] mt-[10px]">{{ paySuccessCustomerNumber }}</div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="12" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div>
            <div class="text-[#000] text-[12px]">会员分布情况</div>
            <Echart :options="pieOptionsData" :height="230" />
          </div>
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="12" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#000] text-[12px]">新增客户趋势</div>
          <Echart :options="newCustomerlineOptionsData" :height="230" />
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="12" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#000] text-[12px]">客户转会员趋势</div>
          <Echart :options="customerConversionLineOptionsData" :height="230" />
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="12" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#000] text-[12px]">支付成功客户趋势</div>
          <Echart :options="paySuccesslineOptionsData" :height="230" />
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="12" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#000] text-[12px]">客户转会员趋势</div>
          <Echart :options="customerConversionLineOptionsData" :height="230" />
        </div>
      </ElSkeleton>
    </ElCol>
    <ElCol :xs="24" :sm="12" class="mb-2">
      <ElSkeleton :loading="loading" animated :rows="4">
        <div class="border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]">
          <div class="text-[#000] text-[12px]">支付成功客户趋势</div>
          <Echart :options="paySuccesslineOptionsData" :height="230" />
        </div>
      </ElSkeleton>
    </ElCol>
  </ElRow>
</template>

<style scoped></style>
