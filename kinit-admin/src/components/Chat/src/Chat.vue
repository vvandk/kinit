<script setup lang="ts">
import { Icon } from '@/components/Icon'
import { propTypes } from '@/utils/propTypes'
import { Dialog } from '@/components/Dialog'
import { ref } from 'vue'
import { useDesign } from '@/hooks/web/useDesign'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('screenfull')

defineProps({
  color: propTypes.string.def('')
})

const dialogVisible = ref(false)
const dialogTitle = ref('聊天室')

const toggleFullscreen = () => {
  dialogVisible.value = true
}
</script>

<template>
  <div :class="prefixCls" @click="toggleFullscreen">
    <Icon :size="18" icon="bi:chat-dots" :color="color" />

    <Dialog v-model="dialogVisible" :title="dialogTitle" :height="650"><div></div> </Dialog>
  </div>
</template>
