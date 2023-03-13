/**
 * 通用js方法封装处理
 * Copyright (c) 2019 ruoyi
 */

/**
 * 获取任意日期
 * date: 时间戳
 * AddDayCount: 在时间戳的基础上加减天数
 * 示例：
 * getDate(new Date(),-3).fullDate  # 三天前的日期
 * getDate(new Date()).fullDate     # 今天的日期
 * getDate(new Date(), 3).fullDate  # 三天后的日期
 */
export function getDate(date, AddDayCount = 0) {
  if (!date) {
    date = new Date()
  }
  if (typeof date !== 'object') {
    date = date.replace(/-/g, '/')
  }
  const dd = new Date(date)

  dd.setDate(dd.getDate() + AddDayCount) // 获取AddDayCount天后的日期

  const y = dd.getFullYear()
  const m = dd.getMonth() + 1 < 10 ? '0' + (dd.getMonth() + 1) : dd.getMonth() + 1 // 获取当前月份的日期，不足10补0
  const d = dd.getDate() < 10 ? '0' + dd.getDate() : dd.getDate() // 获取当前几号，不足10补0
  return {
    fullDate: y + '-' + m + '-' + d,
    year: y,
    month: m,
    date: d,
    day: dd.getDay()
  }
}

// 日期格式化
export function parseTime(time, pattern) {
  if (arguments.length === 0 || !time) {
    return null
  }
  const format = pattern || '{y}-{m}-{d} {h}:{i}:{s}'
  let date
  if (typeof time === 'object') {
    date = time
  } else {
    if (typeof time === 'string' && /^[0-9]+$/.test(time)) {
      time = parseInt(time)
    } else if (typeof time === 'string') {
      time = time.replace(new RegExp(/-/gm), '/')
    }
    if (typeof time === 'number' && time.toString().length === 10) {
      time = time * 1000
    }
    date = new Date(time)
  }
  const formatObj = {
    y: date.getFullYear(),
    m: date.getMonth() + 1,
    d: date.getDate(),
    h: date.getHours(),
    i: date.getMinutes(),
    s: date.getSeconds(),
    a: date.getDay()
  }
  const time_str = format.replace(/{(y|m|d|h|i|s|a)+}/g, (result, key) => {
    let value = formatObj[key]
    // Note: getDay() returns 0 on Sunday
    if (key === 'a') {
      return ['日', '一', '二', '三', '四', '五', '六'][value]
    }
    if (result.length > 0 && value < 10) {
      value = '0' + value
    }
    return value || 0
  })
  return time_str
}

// 表单重置
export function resetForm(refName) {
  if (this.$refs[refName]) {
    this.$refs[refName].resetFields()
  }
}

// 添加日期范围
export function addDateRange(params, dateRange, propName) {
  const search = JSON.parse(JSON.stringify(params))
  if (dateRange != null && dateRange !== '' && dateRange.length !== 0) {
    search.as = JSON.stringify({ create_datetime__range: dateRange })
  }
  return search
}

// 回显数据字典
export function selectDictLabel(datas, value) {
  var actions = []
  Object.keys(datas).some((key) => {
    if (String(datas[key].value) === '' + String(value)) {
      actions.push(datas[key].label)
      return true
    }
  })
  return actions.join('')
}
// 获取字典默认值
export function selectDictDefault(datas) {
  var actions = []
  Object.keys(datas).some((key) => {
    if (datas[key].is_default === true) {
      actions.push(datas[key].dictValue)
      return true
    }
  })
  if (!actions[0] && datas[0]) {
    actions.push(datas[0].dictValue)
  }
  return actions.join('')
}

// 回显数据字典（字符串数组）
export function selectDictLabels(datas, value, separator) {
  var actions = []
  var currentSeparator = undefined === separator ? ',' : separator
  var temp = value.split(currentSeparator)
  Object.keys(value.split(currentSeparator)).some((val) => {
    Object.keys(datas).some((key) => {
      if (datas[key].dictValue == '' + temp[val]) {
        actions.push(datas[key].dictLabel + currentSeparator)
      }
    })
  })
  return actions.join('').substring(0, actions.join('').length - 1)
}

// 转换字符串，undefined,null等转化为""
export function praseStrEmpty(str) {
  if (!str || str == 'undefined' || str == 'null') {
    return ''
  }
  return str
}

// js模仿微信朋友圈计算时间显示几天/几小时/几分钟/刚刚
//datetime 格式为2019-11-22 12:23:59样式
export function timeConversion(datetime) {
  //dateTimeStamp是一个时间毫秒，注意时间戳是秒的形式，在这个毫秒的基础上除以1000，就是十位数的时间戳。13位数的都是时间毫秒。
  // var dateTimeStamp = new Date(datetime.replace(/ /, 'T')).getTime()-8 * 60 * 60 * 1000;//这里要减去中国的时区8小时
  var dateTimeStamp = new Date(datetime.replace(/ /, 'T')).getTime() //这里不减去中国的时区8小时
  var minute = 1000 * 60 //把分，时，天，周，半个月，一个月用毫秒表示
  var hour = minute * 60
  var day = hour * 24
  var week = day * 7
  var month = day * 30
  var now = new Date().getTime() //获取当前时间毫秒
  var diffValue = now - dateTimeStamp //时间差

  if (diffValue < 0) {
    return '刚刚'
  }
  var minC = diffValue / minute //计算时间差的分，时，天，周，月
  var hourC = diffValue / hour
  var dayC = diffValue / day
  var weekC = diffValue / week
  var monthC = diffValue / month
  var result = '2'
  if (monthC >= 1 && monthC <= 3) {
    result = ' ' + parseInt(monthC) + '月前'
  } else if (weekC >= 1 && weekC <= 3) {
    result = ' ' + parseInt(weekC) + '周前'
  } else if (dayC >= 1 && dayC <= 6) {
    result = ' ' + parseInt(dayC) + '天前'
  } else if (hourC >= 1 && hourC <= 23) {
    result = ' ' + parseInt(hourC) + '小时前'
  } else if (minC >= 1 && minC <= 59) {
    result = ' ' + parseInt(minC) + '分钟前'
  } else if (diffValue >= 0 && diffValue <= minute) {
    result = '刚刚'
  } else {
    let datetime = new Date()
    datetime.setTime(dateTimeStamp)
    let Nyear = datetime.getFullYear()
    var Nmonth =
      datetime.getMonth() + 1 < 10 ? '0' + (datetime.getMonth() + 1) : datetime.getMonth() + 1
    var Ndate = datetime.getDate() < 10 ? '0' + datetime.getDate() : datetime.getDate()
    var Nhour = datetime.getHours() < 10 ? '0' + datetime.getHours() : datetime.getHours()
    var Nminute = datetime.getMinutes() < 10 ? '0' + datetime.getMinutes() : datetime.getMinutes()
    var Nsecond = datetime.getSeconds() < 10 ? '0' + datetime.getSeconds() : datetime.getSeconds()
    result = Nyear + '-' + Nmonth + '-' + Ndate
  }
  return result
}
