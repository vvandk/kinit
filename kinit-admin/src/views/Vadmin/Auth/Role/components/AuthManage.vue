<script setup lang="ts">
import {
  ElDrawer,
  ElDivider,
  ElSelect,
  ElOption,
  ElTree,
  ElContainer,
  ElHeader,
  ElAside,
  ElMain,
  ElMessage
} from 'element-plus'
import { ref, nextTick, unref, PropType, watch } from 'vue'
import { Icon } from '@/components/Icon'
import { useDictStore } from '@/store/modules/dict'
import { getMenuRoleTreeOptionsApi } from '@/api/vadmin/auth/menu'
import { getDeptUserTreeOptionsApi } from '@/api/vadmin/auth/dept'
import { eachTree } from '@/utils/tree'
import { isEmptyVal } from '@/utils/is'
import { putRoleListApi } from '@/api/vadmin/auth/role'

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const emit = defineEmits(['getList'])

const data = ref({} as Recordable)

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    data.value = JSON.parse(JSON.stringify(currentRow))
  },
  {
    deep: true,
    immediate: true
  }
)

const drawerVisible = ref(false)

const dataRangeOptions = ref()
const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_data_range'])
  dataRangeOptions.value = dictOptions.sys_vadmin_data_range
}

const defaultProps = {
  children: 'children',
  label: 'label'
}

// 获取部门树
let deptTreeData = ref([] as any[])
const deptTreeRef = ref<InstanceType<typeof ElTree>>()
const getDeptTreeOptions = async () => {
  const res = await getDeptUserTreeOptionsApi()
  if (res) {
    deptTreeData.value = res.data
    await nextTick()
    if (props.currentRow) {
      const dept_ids: number[] = props.currentRow.depts.map((item) => item.id)
      const checked: number[] = []
      // 递归按顺序添加选中的菜单项，用于处理半选状态的菜单项
      eachTree(res.data, (v) => {
        if (dept_ids.includes(v.value)) {
          checked.push(v.value)
        }
      })
      for (const item of checked) {
        unref(deptTreeRef)?.setChecked(item, true, false)
      }
    }
  }
}

// 获取菜单树
let menuTreeData = ref([] as any[])
const menuTreeRef = ref<InstanceType<typeof ElTree>>()
const getMenuRoleTreeOptions = async () => {
  const res = await getMenuRoleTreeOptionsApi()
  if (res) {
    menuTreeData.value = res.data
    await nextTick()
    if (props.currentRow) {
      const menu_ids: number[] = props.currentRow.menus.map((item) => item.id)
      const checked: number[] = []
      // 递归按顺序添加选中的菜单项，用于处理半选状态的菜单项
      eachTree(res.data, (v) => {
        if (menu_ids.includes(v.value)) {
          checked.push(v.value)
        }
      })
      for (const item of checked) {
        unref(menuTreeRef)?.setChecked(item, true, false)
      }
    }
  }
}

const loading = ref(false)

const submit = async () => {
  if (loading.value) return
  if (isEmptyVal(data.value.data_range)) {
    ElMessage.error('数据范围选择项不能为空！')
    return
  }
  loading.value = true
  const menu_ids = [
    ...(unref(menuTreeRef)?.getCheckedKeys() || []),
    ...(unref(menuTreeRef)?.getHalfCheckedKeys() || [])
  ]
  data.value.menu_ids = menu_ids
  data.value.dept_ids = unref(deptTreeRef)?.getCheckedKeys()
  try {
    const res = await putRoleListApi(data.value)
    if (res) {
      loading.value = false
      ElMessage.success('保存成功')
      closeDrawer()
      emit('getList')
    }
  } finally {
    loading.value = false
  }
}

const openDrawer = () => {
  drawerVisible.value = true
  getMenuRoleTreeOptions()
  getDeptTreeOptions()
}

const closeDrawer = () => {
  drawerVisible.value = false
  data.value = {}
  unref(menuTreeRef)?.setCheckedKeys([])
  unref(deptTreeRef)?.setCheckedKeys([])
}

getOptions()

defineExpose({
  openDrawer
})
</script>

<template>
  <div class="auth-manage-main-view">
    <ElDrawer v-model="drawerVisible" :with-header="false" :size="1000" :before-close="closeDrawer">
      <ElContainer>
        <ElHeader>
          <div class="flex justify-between pt-[20px] pb-[20px]">
            <span>权限管理</span>
            <span @click="closeDrawer" class="flex cursor-pointer">
              <Icon icon="iconamoon:close-thin" :size="23" />
            </span>
          </div>
        </ElHeader>
        <ElDivider />
        <div class="h-12 flex justify-between mt-3 mr-3 ml-5">
          <div class="mt-1 text-[#909399]">
            <span>角色名称：{{ data.name }}</span>
          </div>
          <BaseButton type="primary" :loading="loading" @click="submit">保存</BaseButton>
        </div>
        <ElDivider />
        <ElContainer>
          <ElAside width="450px">
            <div class="border-r-1 border-r-[#f0f0f0] b-r-solid h-[100%] p-[20px] box-border">
              <div>
                <div class="flex items-center">
                  <div class="yxt-divider"></div>
                  <span>数据权限</span>
                </div>
                <div class="ml-4 mt-3">
                  <ElSelect v-model="data.data_range" placeholder="请选择数据范围">
                    <ElOption
                      v-for="item in dataRangeOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </ElSelect>
                  <div
                    v-if="data.data_range === '3'"
                    class="mt-3 max-h-[65vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto"
                  >
                    <ElTree
                      ref="deptTreeRef"
                      :data="deptTreeData"
                      show-checkbox
                      node-key="value"
                      :props="defaultProps"
                      :default-expand-all="true"
                      :check-strictly="true"
                    />
                  </div>
                </div>
              </div>
            </div>
          </ElAside>
          <ElMain>
            <div class="flex items-center">
              <div class="yxt-divider"></div>
              <span>菜单权限</span>
            </div>
            <div class="mt-5 max-h-[70vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto box-border">
              <ElTree
                ref="menuTreeRef"
                :data="menuTreeData"
                show-checkbox
                node-key="value"
                :props="defaultProps"
                :default-expand-all="true"
                :check-strictly="false"
              />
            </div>
          </ElMain>
        </ElContainer>
      </ElContainer>
      <ElDivider />

      <!-- <ElDivider /> -->
    </ElDrawer>
  </div>
</template>

<style lang="less">
.auth-manage-main-view .el-drawer .el-drawer__body {
  padding: 0;
}
.auth-manage-main-view .el-divider.el-divider--horizontal {
  margin: 0;
}
</style>

<style scoped lang="less">
.yxt-divider {
  background: #409eff;
  width: 8px;
  height: 20px;
  display: inline-block;
  margin-right: 10px;
}
</style>
