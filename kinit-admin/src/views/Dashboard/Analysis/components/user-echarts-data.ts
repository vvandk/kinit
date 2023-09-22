import { EChartsOption } from 'echarts'
import { useI18n } from '@/hooks/web/useI18n'

const { t } = useI18n()

export const newCustomerlineOptions: EChartsOption = {
  xAxis: {
    data: [
      t('analysis.january'),
      t('analysis.february'),
      t('analysis.march'),
      t('analysis.april'),
      t('analysis.may'),
      t('analysis.june'),
      t('analysis.july'),
      t('analysis.august'),
      t('analysis.september'),
      t('analysis.october'),
      t('analysis.november'),
      t('analysis.december')
    ],
    boundaryGap: true,
    axisTick: {
      show: false // 不限制坐标刻度
    }
  },
  grid: {
    left: 20,
    right: 20,
    bottom: 35,
    top: 30,
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    },
    padding: [5, 10]
  },
  yAxis: {
    type: 'value',
    axisTick: {
      show: false // 不限制坐标刻度
    }
  },
  legend: {
    data: ['新增客户'],
    bottom: -5
  },
  series: [
    {
      name: '新增客户',
      smooth: false, // true 有弧度 ，false 没弧度（直线）
      symbol: 'circle', // 将小圆点改成实心 不写symbol默认空心
      symbolSize: 8, // 小圆点的大小
      type: 'line',
      data: [100, 120, 161, 134, 105, 160, 165, 114, 163, 185, 118, 123],
      animationDuration: 2800,
      animationEasing: 'quadraticOut',
      itemStyle: {
        color: 'rgba(79,168,249)' // 整体颜色
      },
      lineStyle: {
        width: 1, //设置线条粗细
        opacity: 1
      }
    }
  ]
}

export const memberPieOptions: EChartsOption = {
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b} : {c} ({d}%)'
  },
  series: [
    {
      name: '各楼层销售情况统计',
      type: 'pie',
      radius: '60%',
      center: ['50%', '50%'],
      data: [
        { value: 335, name: '青铜卡' },
        { value: 310, name: '白银卡' },
        { value: 234, name: '黄金卡' },
        { value: 135, name: '钻石卡' }
      ]
    }
  ]
}

export const customerConversionLineOptions: EChartsOption = {
  xAxis: {
    data: [
      t('analysis.january'),
      t('analysis.february'),
      t('analysis.march'),
      t('analysis.april'),
      t('analysis.may'),
      t('analysis.june'),
      t('analysis.july'),
      t('analysis.august'),
      t('analysis.september'),
      t('analysis.october'),
      t('analysis.november'),
      t('analysis.december')
    ],
    boundaryGap: true,
    axisTick: {
      show: false // 不限制坐标刻度
    }
  },
  grid: {
    left: 20,
    right: 20,
    bottom: 35,
    top: 30,
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    },
    padding: [5, 10]
  },
  yAxis: {
    type: 'value',
    axisTick: {
      show: false // 不限制坐标刻度
    }
  },
  legend: {
    data: ['转换次数', '转换率'],
    bottom: -5
  },
  series: [
    {
      name: '转换次数',
      smooth: false, // true 有弧度 ，false 没弧度（直线）
      symbol: 'circle', // 将小圆点改成实心 不写symbol默认空心
      symbolSize: 8, // 小圆点的大小
      type: 'line',
      data: [100, 120, 161, 134, 105, 160, 165, 114, 163, 185, 118, 123],
      animationDuration: 2800,
      animationEasing: 'quadraticOut',
      itemStyle: {
        color: 'rgba(110,199,30)' // 整体颜色
      },
      lineStyle: {
        width: 1, //设置线条粗细
        opacity: 1
      }
    },
    {
      name: '转换率',
      smooth: false, // true 有弧度 ，false 没弧度（直线）
      symbol: 'circle', // 将小圆点改成实心 不写symbol默认空心
      symbolSize: 8, // 小圆点的大小
      type: 'line',
      data: [120, 82, 91, 154, 162, 140, 145, 250, 134, 56, 99, 123],
      animationDuration: 2800,
      animationEasing: 'quadraticOut',
      itemStyle: {
        color: 'rgba(79,168,249)' // 整体颜色
      },
      lineStyle: {
        width: 1, //设置线条粗细
        opacity: 1
      }
    }
  ]
}

export const paySuccesslineOptions: EChartsOption = {
  xAxis: {
    data: [
      t('analysis.january'),
      t('analysis.february'),
      t('analysis.march'),
      t('analysis.april'),
      t('analysis.may'),
      t('analysis.june'),
      t('analysis.july'),
      t('analysis.august'),
      t('analysis.september'),
      t('analysis.october'),
      t('analysis.november'),
      t('analysis.december')
    ],
    boundaryGap: true,
    axisTick: {
      show: false // 不限制坐标刻度
    }
  },
  grid: {
    left: 20,
    right: 20,
    bottom: 35,
    top: 30,
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    },
    padding: [5, 10]
  },
  yAxis: {
    type: 'value',
    axisTick: {
      show: false // 不限制坐标刻度
    }
  },
  legend: {
    data: ['支付成功客户数'],
    bottom: -5
  },
  series: [
    {
      name: '支付成功客户数',
      smooth: false, // true 有弧度 ，false 没弧度（直线）
      symbol: 'circle', // 将小圆点改成实心 不写symbol默认空心
      symbolSize: 8, // 小圆点的大小
      type: 'line',
      data: [100, 120, 161, 134, 105, 160, 165, 114, 163, 185, 118, 123],
      animationDuration: 2800,
      animationEasing: 'quadraticOut',
      itemStyle: {
        color: 'rgba(79,168,249)' // 整体颜色
      },
      lineStyle: {
        width: 1, //设置线条粗细
        opacity: 1
      }
    }
  ]
}
