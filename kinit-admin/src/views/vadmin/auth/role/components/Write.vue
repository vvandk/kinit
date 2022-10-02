<script setup lang="ts">
import { Form } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch, ref } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { getMenuRoleTreeOptionsApi } from '@/api/vadmin/auth/menu'
import { schema } from './role.data'
import { ElTree } from 'element-plus'
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
let data = ref([])

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
</script>

<template>
  <Form :rules="rules" @register="register">
    <template #menu_ids>
      <ElTree
        ref="treeRef"
        :data="data"
        show-checkbox
        node-key="value"
        :props="defaultProps"
        :default-checked-keys="defaultCheckedKeys"
      >
        <template #default="{ node }">
          <span>{{ t(node.label) }}</span>
        </template>
      </ElTree>
    </template>
  </Form>
</template>
