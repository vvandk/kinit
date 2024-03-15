<script setup lang="ts">
import { Icon } from '@/components/Icon'
import { propTypes } from '@/utils/propTypes'
import { ElDialog, ElContainer, ElAside, ElHeader, ElMain } from 'element-plus'
import { ref } from 'vue'
import { useDesign } from '@/hooks/web/useDesign'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('screenfull')

defineProps({
  color: propTypes.string.def('')
})

const dialogVisible = ref(false)

const toggleFullscreen = () => {
  dialogVisible.value = true
}
</script>

<template>
  <div :class="prefixCls" @click="toggleFullscreen">
    <Icon :size="18" icon="bi:chat-dots" :color="color" />

    <ElDialog
      v-model="dialogVisible"
      class="chat-dialog !p-[0px]"
      :fullscreen="false"
      destroy-on-close
      lock-scroll
      draggable
      top="8vh"
      width="839px"
      :close-on-click-modal="true"
      :show-close="false"
    >
      <div class="flex justify-start h-[708px]">
        <div class="border-r-solid border-r-1 border-gray-300 w-[200px]"> Aside </div>
        <div>
          <div class="h-[200px]">Header</div>
          <div>Main</div>
        </div>
      </div>
    </ElDialog>
  </div>
</template>

<style lang="less">
.chat-dialog .el-dialog__header {
  display: none;
}

.chat-dialog .el-dialog__body {
  padding: 0px !important;
}
</style>
