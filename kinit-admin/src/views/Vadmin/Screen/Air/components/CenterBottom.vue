<script lang="ts" setup>
import { reactive, PropType, ref, watch } from 'vue'
import { ScrollBoard } from '@kjgl77/datav-vue3'

const props = defineProps({
  centerBottomData: {
    type: Array as PropType<string[][]>,
    required: true
  }
})

const scrollBoardRef = ref<any>(null)

const centerBottomData = ref(props.centerBottomData)

const config = reactive({
  header: ['部门名称', '甲醛', 'PM2.5', 'PM10', '温度', '湿度', '更新时间'],
  data: centerBottomData.value,
  index: true,
  columnWidth: [50],
  align: ['center'],
  rowNum: 6,
  waitTime: 2000,
  headerHeight: 40
})

watch(
  () => props.centerBottomData,
  (val: string[][]) => {
    scrollBoardRef.value.updateRows(val)
  },
  {
    deep: true
  }
)
</script>

<template>
  <div class="center-bottom-view">
    <ScrollBoard ref="scrollBoardRef" :config="config" />
  </div>
</template>

<style lang="less">
.center-bottom-view {
  width: 100%;
  height: 100%;
  margin-top: 20px;

  .dv-scroll-board {
    width: 100%;
    height: 100%;
    color: #fff;

    .header {
      font-size: 18px;
    }

    .rows .row-item {
      font-size: 18px;
    }
  }
}
</style>
