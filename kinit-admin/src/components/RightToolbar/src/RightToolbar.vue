<script setup lang="ts">
import {
  ElButton,
  ElRow,
  ElCol,
  ElDropdownItem,
  ElDropdownMenu,
  ElDropdown,
  ElPopover,
  ElCheckbox,
  ElScrollbar
} from 'element-plus'
import { useIcon } from '@/hooks/web/useIcon'
import { ref, PropType } from 'vue'
import { propTypes } from '@/utils/propTypes'
import draggable from 'vuedraggable'
import { useAppStore } from '@/store/modules/app'
import { useCache } from '@/hooks/web/useCache'

const { wsCache } = useCache()
const appStore = useAppStore()

const emit = defineEmits(['getList', 'update:tableSize'])

const props = defineProps({
  tableSize: propTypes.string.def(''),
  columns: {
    type: Array as PropType<any[]>,
    default: () => []
  },
  cacheTableHeadersKey: propTypes.string.def('')
})

const handleClickRefresh = () => {
  emit('getList')
}

const refresh = useIcon({ icon: 'ic:outline-refresh' })
const spacing = useIcon({ icon: 'mdi:format-paragraph-spacing' })
const settings = useIcon({ icon: 'bytesize:settings' })

const handleCommand = (command: string) => {
  emit('update:tableSize', command)
}

const checkAll = ref(false)
const columns = ref(props.columns)
const isIndeterminate = ref(true) // 如果为True，则表示为半选状态

// 获取表头字段默认列表
if (props.cacheTableHeadersKey) {
  const cacheTableHeaders = wsCache.get(props.cacheTableHeadersKey)
  if (cacheTableHeaders) {
    Object.assign(columns.value, JSON.parse(cacheTableHeaders))
  }
}

const handleCheckAllChange = (val: boolean) => {
  columns.value.forEach((item) => {
    if (item.disabled !== true) {
      item.show = val
    }
  })
  isIndeterminate.value = false
}

const handleCheckChange = () => {
  checkAll.value = columns.value.every((item) => item.show)
  if (checkAll.value) {
    isIndeterminate.value = false
  } else {
    isIndeterminate.value = columns.value.some((item) => item.show)
  }
}
handleCheckChange()

const mobile = appStore.getMobile
</script>

<template>
  <ElRow :gutter="10">
    <ElCol :span="1.5">
      <ElButton link :icon="refresh" @click="handleClickRefresh">{{
        mobile ? '' : '刷新数据'
      }}</ElButton>
    </ElCol>
    <ElCol :span="1.5" class="pt-4px">
      <ElDropdown trigger="click" @command="handleCommand">
        <ElButton link :icon="spacing">{{ mobile ? '' : '密度调整' }}</ElButton>
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem command="default">默认</ElDropdownItem>
            <ElDropdownItem command="large">宽松</ElDropdownItem>
            <ElDropdownItem command="small">紧凑</ElDropdownItem>
          </ElDropdownMenu>
        </template>
      </ElDropdown>
    </ElCol>
    <ElCol :span="1.5">
      <ElPopover placement="bottom" :width="200" trigger="click">
        <div style="border-bottom: 1px solid #d4d7de">
          <el-checkbox
            v-model="checkAll"
            :indeterminate="isIndeterminate"
            @change="handleCheckAllChange"
            >全选</el-checkbox
          >
        </div>
        <ElScrollbar max-height="400px">
          <draggable :list="columns" item-key="field" handle=".cursor-move">
            <template #item="{ element }">
              <div>
                <span class="cursor-move mr-10px">
                  <Icon icon="akar-icons:drag-vertical" />
                </span>
                <ElCheckbox
                  v-model="element.show"
                  :disabled="element.disabled === true"
                  @change="handleCheckChange"
                  >{{ element.label }}</ElCheckbox
                >
              </div>
            </template>
          </draggable>
        </ElScrollbar>
        <template #reference>
          <ElButton link :icon="settings">{{ mobile ? '' : '字段显隐' }}</ElButton>
        </template>
      </ElPopover>
    </ElCol>
  </ElRow>
</template>
