<script lang="ts" setup>
import Left from './components/Left.vue'
import CenterTop from './components/CenterTop.vue'
import CenterBottom from './components/CenterBottom.vue'
import TopMenu from './components/TopMenu.vue'
import { LeftPropsType, CenterTopPropsType } from './typers/index'
import { ref, onBeforeUnmount } from 'vue'
import moment from 'moment'
import { FullScreenContainer, Decoration8 } from '@kjgl77/datav-vue3'

const randomNumber = (min: number, max: number) => {
  return Math.floor(Math.random() * (max - min)) + min
}

const randomNumberStr = (min: number, max: number) => {
  return randomNumber(min, max).toString()
}

const randArray = (len: number, min: number, max: number) => {
  return Array(len)
    .fill(1)
    .map(() => randomNumber(min, max))
}

const leftData = ref({} as LeftPropsType)
const centerBottomData = ref([] as string[][])
const centerTopData = ref({} as CenterTopPropsType)
const menus = ref([] as string[])
const activeIndex = ref(-1)
const activeMenuName = ref('')

const generateData = () => {
  leftData.value = {
    pm25: randomNumberStr(5, 50),
    temp: randomNumberStr(5, 50),
    hum: randomNumberStr(5, 50),
    hcho: randomNumberStr(5, 50)
  }

  menus.value = [
    '技术1部',
    '技术2部',
    '运营部',
    '销售部',
    '人力资源部',
    '技术支持部',
    '客服部',
    '老板办公室'
  ]

  centerBottomData.value = []

  for (let item of menus.value) {
    centerBottomData.value.push([
      item,
      randomNumberStr(5, 50),
      randomNumberStr(5, 50),
      randomNumberStr(5, 50),
      randomNumberStr(5, 50),
      randomNumberStr(5, 50),
      moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
    ])
  }

  centerTopData.value = {
    pm25: randArray(14, 10, 50),
    temp: randArray(14, 10, 50),
    hum: randArray(14, 10, 50),
    hcho: randArray(14, 10, 50)
  }

  activeIndex.value++
  if (activeIndex.value === menus.value.length) {
    activeIndex.value = 0
  }
  activeMenuName.value = menus.value[activeIndex.value]
}

generateData()

const timer = setInterval(() => {
  setTimeout(() => {
    generateData()
  }, 0)
}, 6000)

onBeforeUnmount(() => {
  console.log('已清除定时器')
  clearInterval(timer)
})
</script>

<template>
  <div id="data-view">
    <FullScreenContainer>
      <div class="flex justify-between">
        <div small-bg>
          <Decoration8 style="width: 500px; height: 60px" />
        </div>
        <div class="text-4xl leading-80px font-bold">
          <span>办公室空气质量实时检测</span>
        </div>
        <div small-bg>
          <Decoration8 :reverse="true" style="width: 500px; height: 60px" />
        </div>
      </div>
      <div class="mx-10px my-15px">
        <TopMenu :menus="menus" :activeIndex="activeIndex" />
      </div>
      <div class="h-1/1 overflow-hidden mb-10px ml-10px">
        <div class="float-left w-20/100 h-1/1 mr-20px">
          <Left :leftData="leftData" :activeMenuName="activeMenuName" />
        </div>
        <div class="float-left w-78/100 h-5/10">
          <CenterTop :centerTopData="centerTopData" :activeMenuName="activeMenuName" />
        </div>
        <div class="float-left w-78/100 h-48/100">
          <CenterBottom :centerBottomData="centerBottomData" />
        </div>
      </div>
    </FullScreenContainer>
  </div>
</template>

<style lang="less">
#data-view {
  width: 100%;
  height: 100%;
  background-color: #030409;
  color: #fff;

  #dv-full-screen-container {
    background-image: url('@/assets/imgs/bg.png');
    background-size: 100% 100%;
    box-shadow: 0 0 3px blue;
    display: flex;
    flex-direction: column;
  }
}
</style>
