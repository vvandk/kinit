<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch, ref } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { getMenuRoleTreeOptionsApi } from '@/api/vadmin/auth/menu'
import { schema } from './role.data'
import { ElTree, ElCheckbox } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'

const { required } = useValidator()

const { t } = useI18n()

const props = defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  },
  defaultCheckedKeys: {
    type: Array as PropType<number[]>,
    default: () => []
  }
})

const rules = reactive({
  name: [required()],
  role_key: [required()],
  order: [required()]
})

const { register, methods, elFormRef } = useForm({
  schema: schema
})

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    const { setValues } = methods
    setValues(currentRow)
  },
  {
    deep: true,
    immediate: true
  }
)

const defaultProps = {
  children: 'children',
  label: 'label'
}
let data = ref([] as Recordable[])

const getMenuRoleTreeOptions = async () => {
  const res = await getMenuRoleTreeOptionsApi()
  if (res) {
    data.value = res.data
  }
}

getMenuRoleTreeOptions()

const treeRef = ref<InstanceType<typeof ElTree>>()

const getTreeCheckedKeys = () => {
  return treeRef.value!.getCheckedKeys(false)
}

defineExpose({
  elFormRef,
  getFormData: methods.getFormData,
  getTreeCheckedKeys: getTreeCheckedKeys
})

let selectAll = ref(false)
let defaultExpandAll = ref(true)
let checkStrictly = ref(true) // 父子联动

// 获取所有节点的key
const getTreeNodeKeys = (nodes: Recordable[]): number[] => {
  let keys = [] as number[]
  for (let i = 0; i < nodes.length; i++) {
    keys.push(nodes[i].value)
    if (nodes[i].children && nodes[i].children.length > 0) {
      keys = keys.concat(getTreeNodeKeys(nodes[i].children))
    }
  }
  return keys
}

// 展开/折叠
const handleCheckedTreeExpand = () => {
  for (let i = 0; i < data.value.length; i++) {
    treeRef.value!.store.nodesMap[data.value[i].value].expanded = defaultExpandAll.value
  }
}

//全选/全不选
function handleCheckedTreeNodeAll() {
  treeRef.value!.setCheckedKeys(selectAll.value ? getTreeNodeKeys(data.value) : [])
}
</script>

<template>
  <Form :rules="rules" @register="register">
    <template #menu_ids>
      <div>
        <div>
          <ElCheckbox
            v-model="defaultExpandAll"
            @change="handleCheckedTreeExpand"
            label="展开/折叠"
            size="large"
          />
          <ElCheckbox
            v-model="selectAll"
            @change="handleCheckedTreeNodeAll"
            label="全选/全不选"
            size="large"
          />
          <ElCheckbox v-model="checkStrictly" label="父子联动" size="large" />
        </div>
        <div class="max-h-390px border p-10px overflow-auto">
          <ElTree
            ref="treeRef"
            :data="data"
            show-checkbox
            node-key="value"
            :props="defaultProps"
            :default-expand-all="defaultExpandAll"
            :check-strictly="!checkStrictly"
            :default-checked-keys="defaultCheckedKeys"
          >
            <template #default="{ node }">
              <span>{{ t(node.label) }}</span>
            </template>
          </ElTree>
        </div>
      </div>
    </template>
  </Form>
</template>
