<script setup lang="ts">
import { propTypes } from '@/utils/propTypes'
import { ref } from 'vue'

const props = defineProps({
  modelValue: propTypes.string.def('')
})

const value = ref(props.modelValue)
</script>

<template>
  <span v-html="value"></span>
</template>
