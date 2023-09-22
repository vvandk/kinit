<script lang="ts" setup>
import { propTypes } from '@/utils/propTypes'
import { PropType } from 'vue'
import { LeftPropsType } from '../typers/index'
import { BorderBox11 } from '@kjgl77/datav-vue3'

const props = defineProps({
  leftData: {
    type: Object as PropType<LeftPropsType>,
    required: true
  },
  activeMenuName: propTypes.string
})
</script>

<template>
  <div class="left-view box-border">
    <span class="text-3xl font-bold">{{ props.activeMenuName }}</span>
    <div class="main-content">
      <BorderBox11 title="室内甲醛">
        <div class="data-view">
          <span class="data-title">{{ props.leftData.hcho }}ug/m³</span>
          <span class="data-desc">提示：低于80ug/m³适合长期居住</span>
        </div>
      </BorderBox11>
      <BorderBox11 title="室内PM2.5">
        <div class="data-view">
          <span class="data-title">{{ props.leftData.pm25 }}ug/m³</span>
          <span class="data-desc">提示：低于75ug/m³适合长期居住</span>
        </div>
      </BorderBox11>
      <BorderBox11 title="室内温度">
        <div class="data-view">
          <span class="data-title">{{ props.leftData.temp }}°C</span>
          <span class="data-desc">提示：当前室外温度为25°C</span>
        </div>
      </BorderBox11>
      <BorderBox11 title="室内湿度">
        <div class="data-view">
          <span class="data-title">{{ props.leftData.hum }}%RH</span>
          <span class="data-desc">提示：当前室外湿度为38%RH</span>
        </div>
      </BorderBox11>
    </div>
  </div>
</template>

<style lang="less">
.left-view {
  width: 100%;
  height: 100%;
  box-shadow: 0 0 3px blue;
  display: flex;
  flex-direction: column;
  background-color: rgba(6, 30, 93, 0.5);
  border-top: 2px solid rgba(1, 153, 209, 0.5);
  padding: 10px 20px;

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-top: 10px;

    .dv-border-box-11 {
      .border-box-content {
        justify-content: center;
        align-items: center;
        display: -webkit-flex;
      }

      .data-view {
        position: relative;
        height: 100%;
        width: 100%;
        justify-content: center;
        display: -webkit-flex;

        .data-title {
          font-size: 35px;
          display: block;
          position: absolute;
          top: 40%;
        }

        .data-desc {
          font-size: 14px;
          display: block;
          position: absolute;
          bottom: 10%;
        }
      }
    }
  }
}
</style>
