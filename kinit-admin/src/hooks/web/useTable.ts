import { Table, TableExpose } from '@/components/Table'
import { ElTable, ElMessageBox, ElMessage } from 'element-plus'
import { ref, reactive, watch, computed, unref, nextTick } from 'vue'
import { get } from 'lodash-es'
import type { TableProps } from '@/components/Table/src/types'
import { useI18n } from '@/hooks/web/useI18n'
import { TableSetPropsType } from '@/types/table'
import { isEmpty } from '@/utils/is'

const { t } = useI18n()

interface TableResponse<T = any> {
  count: number
  data: T[]
}

interface UseTableConfig<T = any> {
  getListApi: (option: any) => Promise<IResponse<TableResponse<T>>>
  delListApi?: (option: any) => Promise<IResponse>
  exportQueryListApi?: (params: any, data: any) => Promise<IResponse>
  // 返回数据格式配置
  response: {
    data: string
    count?: string
  }
  // 默认传递的参数
  defaultParams?: Recordable
  props?: TableProps
}

interface TableObject<T = any> {
  limit: number
  page: number
  count: number
  tableData: T[]
  params: any
  loading: boolean
  currentRow: Recordable | null
}

type TableOrderChange = {
  column: Recordable
  prop: string
  order: string | null
}

export const useTable = <T = any>(config?: UseTableConfig<T>) => {
  const tableObject = reactive<TableObject<T>>({
    // 页数
    limit: 10,
    // 当前页
    page: 1,
    // 总条数
    count: 10,
    // 表格数据
    tableData: [],
    // AxiosConfig 配置
    params: {
      ...(config?.defaultParams || {})
    },
    // 加载中
    loading: true,
    // 当前行的数据
    currentRow: null
  })

  const paramsObj = computed(() => {
    return {
      ...tableObject.params,
      limit: tableObject.limit,
      page: tableObject.page
    }
  })

  watch(
    () => tableObject.page,
    () => {
      methods.getList()
    }
  )

  watch(
    () => tableObject.limit,
    () => {
      // 当前页不为1时，修改页数后会导致多次调用getdata方法
      if (tableObject.page === 1) {
        methods.getList()
      } else {
        tableObject.page = 1
        methods.getList()
      }
    }
  )

  // Table实例
  const tableRef = ref<typeof Table & TableExpose>()

  // ElTable实例
  const elTableRef = ref<ComponentRef<typeof ElTable>>()

  const register = (ref: typeof Table & TableExpose, elRef: ComponentRef<typeof ElTable>) => {
    tableRef.value = ref
    elTableRef.value = unref(elRef)
  }

  const getTable = async () => {
    await nextTick()
    const table = unref(tableRef)
    if (!table) {
      console.error('The table is not registered. Please use the register method to register')
    }
    return table
  }

  const delData = async (ids: string[] | number[] | number) => {
    if (config?.delListApi) {
      const res = await config.delListApi(ids)
      if (res) {
        ElMessage.success(t('common.delSuccess'))
        methods.getList()
      }
    } else {
      ElMessage.error('删除失败，请配置删除接口！')
    }
  }

  const methods = {
    getList: async () => {
      tableObject.loading = true
      const res = await config?.getListApi(unref(paramsObj)).finally(() => {
        tableObject.loading = false
      })
      if (res) {
        tableObject.tableData = get(res || {}, config?.response.data as string)
        tableObject.count = get(res || {}, config?.response.count as string) || 0
      }
    },
    setProps: async (props: TableProps = {}) => {
      const table = await getTable()
      table?.setProps(props)
    },
    setColumn: async (columnProps: TableSetPropsType[]) => {
      const table = await getTable()
      table?.setColumn(columnProps)
    },
    getSelections: async () => {
      const table = await getTable()
      return (table?.selections || []) as T[]
    },
    // 设置表格排序
    setOrderParams: (data: TableOrderChange) => {
      tableObject.page = 1
      tableObject.params = Object.assign(tableObject.params, {
        v_order: data.order,
        v_order_field: data.prop
      })
      methods.getList()
    },
    // 与Search组件结合
    setSearchParams: (data: Recordable) => {
      tableObject.page = 1
      tableObject.params = Object.assign(tableObject.params, {
        limit: tableObject.limit,
        page: tableObject.page,
        ...data
      })
      methods.getList()
    },
    // 删除数据
    // 如果存在 ids，则直接使用 ids 中的值进行删除
    // 如果不存在 ids，则判断 multiple 的值来进行删除
    // 如果 multiple 为 true，则说明是多选框，获取多选框中的数据删除
    // 如果为 false，则说明是点击按钮，则获取当前选择行数据进行删除
    delListApi: async (
      multiple: boolean,
      ids: string[] | number[] | number | string = [],
      message = true
    ) => {
      const tableRef = await getTable()
      let value: string[] | number[] | number = []
      if (isEmpty(ids)) {
        if (multiple) {
          if (!tableRef?.selections.length) {
            ElMessage.warning(t('common.delNoData'))
            return
          } else {
            value = tableRef?.selections.map((item) => item.id)
          }
        } else {
          if (!tableObject.currentRow) {
            ElMessage.warning(t('common.delNoData'))
            return
          } else {
            value = tableObject.currentRow.id
          }
        }
      } else {
        value = ids
      }

      if (message) {
        ElMessageBox.confirm(t('common.delMessage'), t('common.delWarning'), {
          confirmButtonText: t('common.delOk'),
          cancelButtonText: t('common.delCancel'),
          type: 'warning'
        }).then(async () => {
          await delData(value)
        })
      } else {
        await delData(value)
      }
    },
    // 导出筛选列表
    exportQueryList: async () => {
      if (config?.exportQueryListApi) {
        const header = config?.props?.columns
          ?.filter((item) => item.show === true)
          .map((item) => {
            return { field: item.field, label: item.label }
          })
        tableObject.loading = true
        const res = await config?.exportQueryListApi(unref(paramsObj), header).finally(() => {
          tableObject.loading = false
        })
        if (res) {
          const a = document.createElement('a')
          a.style.display = 'none'
          a.href = res.data.url
          a.target = '_blank'
          a.download = res.data.filename
          const event = new MouseEvent('click')
          a.dispatchEvent(event)
        }
      } else {
        ElMessage.error('删除失败，请配置删除接口！')
      }
    }
  }

  config?.props && methods.setProps(config.props)

  return {
    register,
    elTableRef,
    tableObject,
    methods
  }
}
