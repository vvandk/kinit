<script setup lang="ts">
import { PropType } from 'vue'
import { Descriptions } from '@/components/Descriptions'
import { DescriptionsSchema } from '@/types/descriptions'

defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  },
  detailSchema: {
    type: Array as PropType<DescriptionsSchema[]>,
    default: () => []
  }
})
</script>

<template>
  <Descriptions :schema="detailSchema" :data="currentRow || {}" />
</template>
