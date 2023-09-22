import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableExpose, TableProps, TableSetProps, TableColumn } from '@/components/Table'
import { ElTable, ElMessageBox, ElMessage } from 'element-plus'
import { ref, watch, unref, nextTick, onMounted } from 'vue'
import { isArray, isEmpty } from '@/utils/is'

const { t } = useI18n()

interface UseTableConfig {
  /**
   * 是否初始化的时候请求一次
   */
  immediate?: boolean
  fetchDataApi: () => Promise<{
    list: any[]
    total?: number
  }>
  fetchDelApi?: (ids: string[] | number[] | number | string) => Promise<boolean>
  fetchExportApi?: (header: Recordable[]) => Promise<IResponse>
}

export const useTable = (config: UseTableConfig) => {
  const { immediate = true } = config

  const loading = ref(false)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const total = ref(0)
  const dataList = ref<any[]>([])

  watch(
    () => currentPage.value,
    () => {
      methods.getList()
    }
  )

  watch(
    () => pageSize.value,
    () => {
      // 当前页不为1时，修改页数后会导致多次调用getList方法
      if (unref(currentPage) === 1) {
        methods.getList()
      } else {
        currentPage.value = 1
        methods.getList()
      }
    }
  )

  onMounted(() => {
    if (immediate) {
      methods.getList()
    }
  })

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

  const methods = {
    /**
     * 获取表单数据
     */
    getList: async () => {
      loading.value = true
      try {
        const res = await config?.fetchDataApi()
        if (res) {
          dataList.value = res.list
          total.value = res.total || 0
        }
      } catch (err) {
        console.log('fetchDataApi error')
      } finally {
        loading.value = false
      }
    },

    /**
     * @description 设置table组件的props
     * @param props table组件的props
     */
    setProps: async (props: TableProps = {}) => {
      const table = await getTable()
      table?.setProps(props)
    },

    /**
     * @description 设置column
     * @param columnProps 需要设置的列
     */
    setColumn: async (columnProps: TableSetProps[]) => {
      const table = await getTable()
      table?.setColumn(columnProps)
    },

    /**
     * @description 新增column
     * @param tableColumn 需要新增数据
     * @param index 在哪里新增
     */
    addColumn: async (tableColumn: TableColumn, index?: number) => {
      const table = await getTable()
      table?.addColumn(tableColumn, index)
    },

    /**
     * @description 删除column
     * @param field 删除哪个数据
     */
    delColumn: async (field: string) => {
      const table = await getTable()
      table?.delColumn(field)
    },

    /**
     * @description 获取ElTable组件的实例
     * @returns ElTable instance
     */
    getElTableExpose: async () => {
      await getTable()
      return unref(elTableRef)
    },

    refresh: () => {
      methods.getList()
    },

    // sortableChange: (e: any) => {
    //   console.log('sortableChange', e)
    //   const { oldIndex, newIndex } = e
    //   dataList.value.splice(newIndex, 0, dataList.value.splice(oldIndex, 1)[0])
    //   // to do something
    // }

    // 删除数据
    // 如果存在 ids，则直接使用 ids 中的值进行删除
    // 如果不存在 ids，则判断 multiple 的值来进行删除
    // 如果 multiple 为 true，则说明是多选框，获取多选框中的数据删除
    // 如果为 false，则说明是点击按钮，则必须传递当前选择行的值
    delList: async (
      multiple: boolean,
      ids: string[] | number[] | number | string = [],
      message = true
    ) => {
      const { fetchDelApi } = config
      if (!fetchDelApi) {
        console.warn('fetchDelApi 方法未定义！')
        return
      }
      await getTable()
      let value: string[] | number[] | number | string = []
      if (isEmpty(ids)) {
        if (multiple) {
          if (unref(elTableRef)?.getSelectionRows().length > 0) {
            value = unref(elTableRef)
              ?.getSelectionRows()
              .map((item) => item.id)
          } else {
            ElMessage.warning(t('common.delNoData'))
            return
          }
        } else {
          ElMessage.warning(t('common.delNoData'))
          return
        }
      } else {
        value = ids
      }

      const handleResule = () => {
        ElMessage.success(t('common.delSuccess'))

        const idsLength = isArray(value) ? value.length : 1

        // 计算出临界点
        const current =
          unref(total) % unref(pageSize) === idsLength || unref(pageSize) === 1
            ? unref(currentPage) > 1
              ? unref(currentPage) - 1
              : unref(currentPage)
            : unref(currentPage)

        currentPage.value = current
        methods.getList()
      }

      if (message) {
        ElMessageBox.confirm(t('common.delMessage'), t('common.delWarning'), {
          confirmButtonText: t('common.delOk'),
          cancelButtonText: t('common.delCancel'),
          type: 'warning'
        }).then(async () => {
          const result = await fetchDelApi(value)
          if (result) {
            handleResule()
          }
        })
      } else {
        const result = await fetchDelApi(value)
        if (result) {
          handleResule()
        }
      }
    },

    getSelections: async () => {
      await getTable()
      return (unref(elTableRef)?.getSelectionRows() || []) as any[]
    },

    // 导出筛选列表
    exportQueryList: async (headers?: any[]) => {
      const { fetchExportApi } = config
      if (!fetchExportApi) {
        console.warn('fetchExportApi 方法未定义！')
        return
      }

      if (!headers) {
        const table = await getTable()
        headers = table!
          .getColumn()
          .filter((item) => item.show === true && item.type !== 'selection')
          .map((item) => {
            return { field: item.field, label: item.label }
          })
      }

      try {
        loading.value = true
        const res = await fetchExportApi(headers)
        if (res) {
          const a = document.createElement('a')
          a.style.display = 'none'
          a.href = res.data.url
          a.target = '_blank'
          a.download = res.data.filename
          const event = new MouseEvent('click')
          a.dispatchEvent(event)
        }
      } catch (err) {
        console.log('fetchExportApi error')
      } finally {
        loading.value = false
      }
    }
  }

  return {
    tableRegister: register,
    tableMethods: methods,
    tableState: {
      currentPage,
      pageSize,
      total,
      dataList,
      loading
    }
  }
}
