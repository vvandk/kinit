<script setup>
import { ElDescriptions, ElDescriptionsItem } from 'element-plus'
import { ref } from 'vue'

const cronExample = ref([
  {
    value: '0 0 10,15,16 * * ?',
    label: '每天上午10点，下午3点，4点'
  },
  {
    value: '0 0/30 9-17 * * ?',
    label: '朝九晚五工作时间内每半小时'
  },
  {
    value: '0 0 12 ? * WED	',
    label: '表示每个星期三中午12点'
  },
  {
    value: '0 0 12 * * ?',
    label: '每天中午12点触发'
  },
  {
    value: '0 15 10 ? * *',
    label: '每天上午10:15触发'
  },
  {
    value: '0 15 10 * * ?',
    label: '每天上午10:15触发 （跟上面的一样）'
  },
  {
    value: '0 15 10 * * ? 2005',
    label: '2005年的每天上午10:15触发'
  },
  {
    value: '0 * 14 * * ?',
    label: '在每天下午2点到下午2:59期间的每1分钟触发'
  },
  {
    value: '0 0/5 14 * * ?',
    label: '在每天下午2点到下午2:55期间的每5分钟触发'
  },
  {
    value: '0 0/5 14,18 * * ?',
    label: '在每天下午2点到2:55期间和下午6点到6:55期间的每5分钟触发'
  },
  {
    value: '0 0-5 14 * * ?',
    label: '在每天下午2点到下午2:05期间的每1分钟触发'
  },
  {
    value: '0 10,44 14 ? 3 WED',
    label: '每年三月的星期三的下午2:10和2:44触发'
  },
  {
    value: '0 15 10 ? * MON-FRI',
    label: '周一至周五的上午10:15触发'
  },
  {
    value: '0 15 10 15 * ?',
    label: '每月15日上午10:15触发'
  },
  {
    value: '0 15 10 L * ?',
    label: '每月最后一日的上午10:15触发'
  }
])
</script>

<template>
  <ElDescriptions :column="1" :border="true">
    <ElDescriptionsItem v-for="(item, index) in cronExample" :key="index" :label="item.value">{{
      item.label
    }}</ElDescriptionsItem>
  </ElDescriptions>
</template>

<style lang="scss" scoped></style>
