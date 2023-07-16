<script setup lang="ts">
import { ref } from 'vue'
import {
  ElTabs,
  ElTabPane,
  ElRadioGroup,
  ElRadio,
  ElInput,
  ElCheckboxGroup,
  ElCheckbox,
  ElTable,
  ElTableColumn,
  ElButton,
  ElMessage
} from 'element-plus'
import type { TableColumnCtx } from 'element-plus'
import cron from 'cron-validate'
import { Dialog } from '@/components/Dialog'
import RunDatetimeList from './RunDatetimeList.vue'
import CronExample from './CronExample.vue'

const activeName = ref('seconds')

const tableData = ref([
  {
    title: '表达式字段',
    seconds: '*',
    minutes: '*',
    hour: '*',
    day: '*',
    month: '*',
    week: '?',
    year: ''
  },
  {
    title: 'Cron 表达式',
    seconds: '* * * * * ?',
    minutes: '',
    hour: '',
    day: '',
    month: '',
    week: '',
    year: ''
  }
])

const seconds = ref('0')
const seconds1_1 = ref()
const seconds1_2 = ref()
const seconds2_1 = ref()
const seconds2_2 = ref()
const seconds3_1 = ref()

// 秒改变事件
const secondsChange = () => {
  const secondsValue = ref('*')
  if (seconds.value === '1' && seconds1_1.value && seconds1_2.value) {
    secondsValue.value = `${seconds1_1.value}-${seconds1_2.value}`
  } else if (seconds.value === '2' && seconds2_1.value && seconds2_2.value) {
    secondsValue.value = `${seconds2_1.value}/${seconds2_2.value}`
  } else if (seconds.value === '3' && seconds3_1.value) {
    secondsValue.value = seconds3_1.value.join(',')
  }
  tableData.value[0].seconds = secondsValue.value
  fieldToCron(tableData.value[0])
}

const minutes = ref('0')
const minutes1_1 = ref()
const minutes1_2 = ref()
const minutes2_1 = ref()
const minutes2_2 = ref()
const minutes3_1 = ref()

// 分改变事件
const minutesChange = () => {
  const minutesValue = ref('*')
  if (minutes.value === '1' && minutes1_1.value && minutes1_2.value) {
    minutesValue.value = `${minutes1_1.value}-${minutes1_2.value}`
  } else if (minutes.value === '2' && minutes2_1.value && minutes2_2.value) {
    minutesValue.value = `${minutes2_1.value}/${minutes2_2.value}`
  } else if (minutes.value === '3' && minutes3_1.value) {
    minutesValue.value = minutes3_1.value.join(',')
  }
  tableData.value[0].minutes = minutesValue.value
  fieldToCron(tableData.value[0])
}

const hour = ref('0')
const hour1_1 = ref()
const hour1_2 = ref()
const hour2_1 = ref()
const hour2_2 = ref()
const hour3_1 = ref()

// 小时改变事件
const hourChange = () => {
  const hourValue = ref('*')
  if (hour.value === '1' && hour1_1.value && hour1_2.value) {
    hourValue.value = `${hour1_1.value}-${hour1_2.value}`
  } else if (hour.value === '2' && hour2_1.value && hour2_2.value) {
    hourValue.value = `${hour2_1.value}/${hour2_2.value}`
  } else if (hour.value === '3' && hour3_1.value) {
    hourValue.value = hour3_1.value.join(',')
  }
  tableData.value[0].hour = hourValue.value
  fieldToCron(tableData.value[0])
}

const day = ref('0')
const day1_1 = ref()
const day1_2 = ref()
const day2_1 = ref()
const day2_2 = ref()
const day3_1 = ref()
const day4_1 = ref()

// 日改变事件
const dayChange = () => {
  const dayValue = ref('*')
  if (day.value === '1') {
    dayValue.value = '?'
  } else if (day.value === '2') {
    dayValue.value = 'L'
  } else if (day.value === '3' && day1_1.value && day1_2.value) {
    dayValue.value = `${day1_1.value}-${day1_2.value}`
  } else if (day.value === '4' && day2_1.value && day2_2.value) {
    dayValue.value = `${day2_1.value}/${day2_2.value}`
  } else if (day.value === '5' && day3_1.value) {
    dayValue.value = `${day3_1.value}W`
  } else if (day.value === '6' && day4_1.value) {
    dayValue.value = day4_1.value.join(',')
  }
  tableData.value[0].day = dayValue.value
  if (day.value !== '1') {
    week.value = '1'
    tableData.value[0].week = '?'
  }
  fieldToCron(tableData.value[0])
}

const month = ref('0')
const month1_1 = ref()
const month1_2 = ref()
const month2_1 = ref()
const month2_2 = ref()
const month3_1 = ref()

// 月改变事件
const monthChange = () => {
  const monthValue = ref('*')
  if (month.value === '1' && month1_1.value && month1_2.value) {
    monthValue.value = `${month1_1.value}-${month1_2.value}`
  } else if (month.value === '2' && month2_1.value && month2_2.value) {
    monthValue.value = `${month2_1.value}/${month2_2.value}`
  } else if (month.value === '3' && month3_1.value) {
    monthValue.value = month3_1.value.join(',')
  }
  tableData.value[0].month = monthValue.value
  fieldToCron(tableData.value[0])
}

const weekListData = ref(['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'])
const week = ref('1')
const week1_1 = ref()
const week1_2 = ref()
const week2_1 = ref()
const week2_2 = ref()
const week3_1 = ref()
const week4_1 = ref()

// 周改变事件
const weekChange = () => {
  const weekValue = ref('*')
  if (week.value === '1') {
    weekValue.value = '?'
  } else if (week.value === '2' && week1_1.value && week1_2.value) {
    weekValue.value = `${week1_1.value}-${week1_2.value}`
  } else if (week.value === '3' && week2_1.value && week2_2.value) {
    weekValue.value = `${week2_1.value}#${week2_2.value}`
  } else if (week.value === '4' && week3_1.value) {
    weekValue.value = `${week3_1.value}L`
  } else if (week.value === '5' && week4_1.value) {
    weekValue.value = week4_1.value.join(',')
  }
  tableData.value[0].week = weekValue.value
  if (week.value !== '1') {
    day.value = '1'
    tableData.value[0].day = '?'
  }
  fieldToCron(tableData.value[0])
}

const year = ref()
const year1_1 = ref()
const year1_2 = ref()

// 年改变事件
const yearChange = () => {
  const yearValue = ref('')
  if (year.value === '0') {
    yearValue.value = '*'
  } else if (year.value === '1') {
    yearValue.value = ''
  } else if (year.value === '2' && year1_1.value && year1_2.value) {
    yearValue.value = `${year1_1.value}-${year1_2.value}`
  }
  tableData.value[0].year = yearValue.value
  fieldToCron(tableData.value[0])
}

interface SpanMethodProps {
  row: any
  column: TableColumnCtx<any>
  rowIndex: number
  columnIndex: number
}

// 表格合并单元格
const arraySpanMethod = ({ row, column, rowIndex, columnIndex }: SpanMethodProps) => {
  if (rowIndex === 1 && columnIndex >= 1 && columnIndex <= 6) {
    return {
      rowspan: 1,
      colspan: 6
    }
  }
}

// 表达式字段 转 Cron 表达式
const fieldToCron = (row) => {
  const seconds = row.seconds !== '' ? row.seconds : '*'
  const minutes = row.minutes !== '' ? row.minutes : '*'
  const hour = row.hour !== '' ? row.hour : '*'
  const day = row.day !== '' ? row.day : '*'
  const month = row.month !== '' ? row.month : '*'
  const week = row.week !== '' ? row.week : '?'
  const year = row.year !== '' ? row.year : ''

  const cron = ref(`${seconds} ${minutes} ${hour} ${day} ${month} ${week} ${year}`)
  tableData.value[1].seconds = cron.value.trim()
}

// Cron 表达式 转 表达式字段
const cronToField = () => {
  const cronExpression = tableData.value[1].seconds // 获取 Cron 表达式
  const [seconds, minutes, hour, day, month, week, year] = cronExpression.split(' ')

  // 更新表达式字段的值
  tableData.value[0].seconds = seconds
  tableData.value[0].minutes = minutes
  tableData.value[0].hour = hour
  tableData.value[0].day = day
  tableData.value[0].month = month
  tableData.value[0].week = week
  tableData.value[0].year = year
}

// 验证 cron 表达式
// https://blog.csdn.net/a2524289/article/details/109177764
// 生成工具：https://cron.qqe2.com/
// cron 表达式转中文描述：https://github.com/bradymholt/cRonstrue
// cronjs 解析器与匹配器(五位)：https://github.com/datasert/cronjs
// cron 表达式验证器：https://github.com/Airfooox/cron-validate
const validate = () => {
  const cronExpression = tableData.value[1].seconds // 获取 Cron 表达式
  const fields = cronExpression.split(' ')
  const [seconds, minutes, hour, day, month, week, year] = fields
  let useYears = true

  if (fields.length === 6) {
    useYears = false
  } else if (fields.length === 7) {
    useYears = true
  } else {
    ElMessage.error('验证失败')
    return
  }
  // 验证字段是否为空
  if (!seconds || !minutes || !hour || !day || !month || !week) {
    ElMessage.error('验证失败')
    return
  }

  // 验证日字段和周字段的冲突
  if (day === '?' && week === '?') {
    ElMessage.error('验证失败')
    return
  }
  const result = cron(cronExpression, {
    override: {
      useSeconds: true,
      useYears: useYears,
      useBlankDay: true,
      useLastDayOfMonth: true,
      useLastDayOfWeek: true,
      useNearestWeekday: true,
      useNthWeekdayOfMonth: true
    }
  }).isValid()
  if (result) {
    ElMessage.success('验证成功')
  } else {
    ElMessage.error('验证失败')
  }
}

const dialogVisible1 = ref(false)
const dialogVisible2 = ref(false)

// 获取最近十次运行时间
const getRunDatetime = () => {
  dialogVisible1.value = true
}

// Cron 表达式示例
const getCronExample = () => {
  dialogVisible2.value = true
}
</script>

<template>
  <div class="cron-expression-box">
    <ElTabs v-model="activeName" type="border-card">
      <ElTabPane label="秒" name="seconds">
        <ElRadioGroup class="!block" v-model="seconds" @change="secondsChange">
          <div class="list-item">
            <ElRadio label="0">每秒</ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio label="1">
              <ElInput v-model="seconds1_1" @change="secondsChange" class="!w-[300px]">
                <template #prepend> 周期从 </template>
              </ElInput>
              <ElInput v-model="seconds1_2" @change="secondsChange" class="!w-[300px]">
                <template #prepend> - </template>
                <template #append>秒</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="2">
              <ElInput v-model="seconds2_1" @change="secondsChange" class="!w-[200px]">
                <template #prepend> 从 </template>
              </ElInput>
              <ElInput v-model="seconds2_2" @change="secondsChange" class="!w-[400px]">
                <template #prepend> 秒开始，每 </template>
                <template #append>秒执行一次</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio class="!whitespace-normal !inline" label="3">
              <span>指定</span>
              <ElCheckboxGroup class="ml-6" v-model="seconds3_1" @change="secondsChange">
                <ElCheckbox v-for="(num, index) in 60" :key="num" :label="index.toString()" />
              </ElCheckboxGroup>
            </ElRadio>
          </div>
        </ElRadioGroup>
      </ElTabPane>
      <ElTabPane label="分" name="minutes">
        <ElRadioGroup class="!block" v-model="minutes" @change="minutesChange">
          <div class="list-item">
            <ElRadio label="0">每分</ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio label="1">
              <ElInput v-model="minutes1_1" @change="minutesChange" class="!w-[300px]">
                <template #prepend> 周期从 </template>
              </ElInput>
              <ElInput v-model="minutes1_2" @change="minutesChange" class="!w-[300px]">
                <template #prepend> - </template>
                <template #append>分</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="2">
              <ElInput v-model="minutes2_1" @change="minutesChange" class="!w-[200px]">
                <template #prepend> 从 </template>
              </ElInput>
              <ElInput v-model="minutes2_2" @change="minutesChange" class="!w-[400px]">
                <template #prepend> 分开始，每 </template>
                <template #append>分执行一次</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio class="!whitespace-normal !inline" label="3">
              <span>指定</span>
              <ElCheckboxGroup class="ml-6" v-model="minutes3_1" @change="minutesChange">
                <ElCheckbox v-for="(num, index) in 60" :key="num" :label="index.toString()" />
              </ElCheckboxGroup>
            </ElRadio>
          </div>
        </ElRadioGroup>
      </ElTabPane>
      <ElTabPane label="时" name="hour">
        <ElRadioGroup class="!block" v-model="hour" @change="hourChange">
          <div class="list-item">
            <ElRadio label="0">每小时</ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio label="1">
              <ElInput v-model="hour1_1" @change="hourChange" class="!w-[300px]">
                <template #prepend> 周期从 </template>
              </ElInput>
              <ElInput v-model="hour1_2" @change="hourChange" class="!w-[300px]">
                <template #prepend> - </template>
                <template #append>小时</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="2">
              <ElInput v-model="hour2_1" @change="hourChange" class="!w-[200px]">
                <template #prepend> 从 </template>
              </ElInput>
              <ElInput v-model="hour2_2" @change="hourChange" class="!w-[400px]">
                <template #prepend> 小时开始，每 </template>
                <template #append>小时执行一次</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio class="!whitespace-normal !inline" label="3">
              <span>指定</span>
              <ElCheckboxGroup class="ml-6" v-model="hour3_1" @change="hourChange">
                <ElCheckbox v-for="(num, index) in 24" :key="num" :label="index.toString()" />
              </ElCheckboxGroup>
            </ElRadio>
          </div>
        </ElRadioGroup>
      </ElTabPane>
      <ElTabPane label="日" name="day">
        <ElRadioGroup class="!block" v-model="day" @change="dayChange">
          <div class="list-item">
            <ElRadio label="0">每天</ElRadio>
          </div>
          <div class="list-item">
            <ElRadio label="1">不指定</ElRadio>
          </div>
          <div class="list-item">
            <ElRadio label="2">月最后一天</ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio label="3">
              <ElInput v-model="day1_1" @change="dayChange" class="!w-[300px]">
                <template #prepend> 周期从 </template>
              </ElInput>
              <ElInput v-model="day1_2" @change="dayChange" class="!w-[300px]">
                <template #prepend> - </template>
                <template #append>日</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="4">
              <ElInput v-model="day2_1" @change="dayChange" class="!w-[200px]">
                <template #prepend> 从 </template>
              </ElInput>
              <ElInput v-model="day2_2" @change="dayChange" class="!w-[400px]">
                <template #prepend> 日开始，每 </template>
                <template #append>日执行一次</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="5">
              <ElInput v-model="day3_1" @change="dayChange" class="!w-[600px]">
                <template #prepend> 每月 </template>
                <template #append>号最近的那个工作日</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio class="!whitespace-normal !inline" label="6">
              <span>指定</span>
              <ElCheckboxGroup class="ml-6" v-model="day4_1" @change="dayChange">
                <ElCheckbox v-for="num in 31" :key="num" :label="num" />
              </ElCheckboxGroup>
            </ElRadio>
          </div>
        </ElRadioGroup>
      </ElTabPane>
      <ElTabPane label="月" name="month">
        <ElRadioGroup class="!block" v-model="month" @change="monthChange">
          <div class="list-item">
            <ElRadio label="0">每月</ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio label="1">
              <ElInput v-model="month1_1" @change="monthChange" class="!w-[300px]">
                <template #prepend> 周期从 </template>
              </ElInput>
              <ElInput v-model="month1_2" @change="monthChange" class="!w-[300px]">
                <template #prepend> - </template>
                <template #append>月</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="2">
              <ElInput v-model="month2_1" @change="monthChange" class="!w-[200px]">
                <template #prepend> 从 </template>
              </ElInput>
              <ElInput v-model="month2_2" @change="monthChange" class="!w-[400px]">
                <template #prepend> 月开始，每 </template>
                <template #append>月执行一次</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio class="!whitespace-normal !inline" label="3">
              <span>指定</span>
              <ElCheckboxGroup class="ml-6" v-model="month3_1" @change="monthChange">
                <ElCheckbox v-for="num in 12" :key="num" :label="num" />
              </ElCheckboxGroup>
            </ElRadio>
          </div>
        </ElRadioGroup>
      </ElTabPane>
      <ElTabPane label="周" name="week">
        <ElRadioGroup class="!block" v-model="week" @change="weekChange">
          <div class="list-item">
            <ElRadio label="0">每周</ElRadio>
          </div>
          <div class="list-item">
            <ElRadio label="1">不指定</ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio label="2">
              <ElInput v-model="week1_1" @change="weekChange" class="!w-[300px]">
                <template #prepend> 周期从星期 </template>
              </ElInput>
              <ElInput v-model="week1_2" @change="weekChange" class="!w-[300px]">
                <template #prepend> - 星期</template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="3">
              <ElInput v-model="week2_1" @change="weekChange" class="!w-[300px]">
                <template #prepend> 第 </template>
              </ElInput>
              <ElInput v-model="week2_2" @change="weekChange" class="!w-[300px]">
                <template #prepend> 星期的星期 </template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-4">
            <ElRadio label="4">
              <ElInput v-model="week3_1" @change="weekChange" class="!w-[600px]">
                <template #prepend> 本月最后一个星期 </template>
              </ElInput>
            </ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio class="!whitespace-normal !inline" label="5">
              <span>指定</span>
              <ElCheckboxGroup class="ml-6" v-model="week4_1" @change="weekChange">
                <ElCheckbox v-for="(item, index) in weekListData" :key="index" :label="index">{{
                  item
                }}</ElCheckbox>
              </ElCheckboxGroup>
            </ElRadio>
          </div>
        </ElRadioGroup>
      </ElTabPane>
      <ElTabPane label="年" name="year">
        <ElRadioGroup class="!block" v-model="year" @change="yearChange">
          <div class="list-item">
            <ElRadio label="0">每年</ElRadio>
          </div>
          <div class="list-item">
            <ElRadio label="1">不指定</ElRadio>
          </div>
          <div class="list-item mt-2">
            <ElRadio label="2">
              <ElInput v-model="year1_1" @change="yearChange" class="!w-[300px]">
                <template #prepend> 周期从 </template>
              </ElInput>
              <ElInput v-model="year1_2" @change="yearChange" class="!w-[300px]">
                <template #prepend> - </template>
                <template #append> 年 </template>
              </ElInput>
            </ElRadio>
          </div>
        </ElRadioGroup>
      </ElTabPane>
    </ElTabs>
    <div class="mt-5">
      <span class="text-[17px]">生成表达式</span>
      <ElTable
        :data="tableData"
        style="width: 100%"
        :span-method="arraySpanMethod"
        class="mt-2"
        :border="true"
      >
        <ElTableColumn prop="title" label="" />
        <ElTableColumn prop="seconds" label="秒" align="center">
          <template #default="{ row, $index }">
            <ElInput v-if="$index === 0" v-model="row.seconds" @change="fieldToCron(row)" />
            <ElInput v-if="$index === 1" v-model="row.seconds" />
          </template>
        </ElTableColumn>
        <ElTableColumn prop="minutes" label="分钟" align="center">
          <template #default="{ row, $index }">
            <ElInput v-if="$index === 0" v-model="row.minutes" @change="fieldToCron(row)" />
            <ElButton v-if="$index === 1" type="primary" link @click="cronToField">
              解析为字段
            </ElButton>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="hour" label="小时" align="center">
          <template #default="{ row, $index }">
            <ElInput v-if="$index === 0" v-model="row.hour" @change="fieldToCron(row)" />
          </template>
        </ElTableColumn>
        <ElTableColumn prop="day" label="日" align="center">
          <template #default="{ row, $index }">
            <ElInput v-if="$index === 0" v-model="row.day" @change="fieldToCron(row)" />
          </template>
        </ElTableColumn>
        <ElTableColumn prop="month" label="月" align="center">
          <template #default="{ row, $index }">
            <ElInput v-if="$index === 0" v-model="row.month" @change="fieldToCron(row)" />
          </template>
        </ElTableColumn>
        <ElTableColumn prop="week" label="星期" align="center">
          <template #default="{ row, $index }">
            <ElInput v-if="$index === 0" v-model="row.week" @change="fieldToCron(row)" />
          </template>
        </ElTableColumn>
        <ElTableColumn prop="year" label="年" align="center">
          <template #default="{ row, $index }">
            <ElInput v-if="$index === 0" v-model="row.year" @change="fieldToCron(row)" />
          </template>
        </ElTableColumn>
      </ElTable>
      <div class="mt-3 text-center">
        <ElButton type="primary" @click="getRunDatetime">获取最近十次运行时间</ElButton>
        <ElButton type="primary" @click="validate">Cron 表达式验证</ElButton>
        <ElButton type="primary" @click="getCronExample">Cron 表达式示例</ElButton>
      </div>
    </div>
  </div>

  <Dialog
    v-model="dialogVisible1"
    title="获取最近十次运行时间"
    width="600px"
    height="400px"
    top="13vh"
  >
    <RunDatetimeList :expression="tableData[1].seconds" />
  </Dialog>

  <Dialog v-model="dialogVisible2" title="Cron 表达式示例" width="700px" height="620px" top="12vh">
    <CronExample />
  </Dialog>
</template>

<style lang="less">
.cron-expression-box {
  .el-input {
    .el-input-group__prepend {
      border-radius: 0;
    }

    .el-input-group__append {
      border-radius: 0;
    }

    .el-input__wrapper {
      border-radius: 0;
    }
  }
}
</style>
