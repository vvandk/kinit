<script lang="ts" setup>
import { propTypes } from '@/utils/propTypes'
import { PropType } from 'vue'
import { BorderBox10, Decoration7 } from '@kjgl77/datav-vue3'

const props = defineProps({
  menus: {
    type: Array as PropType<string[]>,
    required: true
  },
  activeIndex: propTypes.number
})
</script>

<template>
  <div class="top-menu-view">
    <BorderBox10>
      <div class="menu-item-view" v-for="(item, index) in props.menus" :key="index">
        <Decoration7
          class="animate__animated animate__fadeInDown"
          v-if="index === props.activeIndex"
        >
          {{ item }}
        </Decoration7>
        <span v-else>{{ item }}</span>
      </div>
    </BorderBox10>
  </div>
</template>

<style lang="less">
.top-menu-view {
  .dv-border-box-10 {
    height: 80px;
    overflow: hidden;

    .menu-item-view {
      float: left;
      line-height: 80px;
      margin: 0 30px;
      font-size: 22px;
      color: #909399;
      font-weight: bold;

      &:first-of-type {
        margin-left: 50px;
      }

      .dv-decoration-7 {
        height: 100%;
        color: #fff;
      }
    }
  }
}
</style>
