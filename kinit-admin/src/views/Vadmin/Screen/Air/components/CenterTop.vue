<script lang="ts" setup>
import { Echart } from '@/components/Echart'
import { propTypes } from '@/utils/propTypes'
import { PropType, ref, watch } from 'vue'
import { CenterTopPropsType } from '../typers'

const props = defineProps({
  centerTopData: {
    type: Object as PropType<CenterTopPropsType>,
    required: true
  },
  activeMenuName: propTypes.string
})

const lineOptions = ref({})

watch(
  () => props.centerTopData,
  (val: CenterTopPropsType) => {
    lineOptions.value = {
      xAxis: {
        data: [
          '6H',
          '7H',
          '8H',
          '9H',
          '10H',
          '11H',
          '12H',
          '13H',
          '14H',
          '15H',
          '16H',
          '17H',
          '18H',
          '19H'
        ],
        type: 'category'
      },
      textStyle: {
        fontFamily: 'Microsoft YaHei',
        fontSize: 20,
        fontStyle: 'normal',
        fontWeight: 'normal',
        color: '#ecc460'
      },
      grid: {
        left: 20,
        right: 20,
        bottom: 20,
        top: 80,
        containLabel: true
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        padding: [5, 10]
      },
      yAxis: [
        {
          type: 'value',
          name: '',
          min: 0,
          axisLabel: {
            formatter: '{value}'
          }
        }
      ],
      legend: {
        data: ['PM2.5', '甲醛', '温度', '湿度'],
        // top: 50,
        textStyle: {
          color: '#c3f19d'
        }
      },
      series: [
        {
          name: 'PM2.5',
          type: 'bar',
          color: '#bbff67',
          emphasis: {
            focus: 'series'
          },
          data: val.pm25,
          showBackground: false,
          barGap: 0
        },
        {
          name: '甲醛',
          type: 'bar',
          color: '#6deedf',
          emphasis: {
            focus: 'series'
          },
          data: val.hcho,
          showBackground: false,
          barGap: 0
        },
        {
          name: '温度',
          type: 'line',
          emphasis: {
            focus: 'series'
          },
          data: val.temp
        },
        {
          name: '湿度',
          type: 'line',
          emphasis: {
            focus: 'series'
          },
          data: val.hum
        }
      ]
    }
  },
  {
    immediate: true,
    deep: true
  }
)
</script>

<template>
  <div class="center-top-view">
    <span class="text-3xl font-bold">{{ props.activeMenuName }}</span>
    <div>
      <Echart :options="lineOptions" :height="400" />
    </div>
  </div>
</template>

<style lang="less">
.center-top-view {
  width: 100%;
  height: 100%;
  box-shadow: 0 0 3px blue;
  display: flex;
  flex-direction: column;
  background-color: rgba(6, 30, 93, 0.5);
  border-top: 2px solid rgba(1, 153, 209, 0.5);
  box-sizing: border-box;
  padding: 10px 20px;
}
</style>
