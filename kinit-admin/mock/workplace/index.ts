import { config } from '@/config/axios/config'
import { MockMethod } from 'vite-plugin-mock'

const { result_code } = config

const timeout = 1000

export default [
  // 获取统计
  {
    url: '/api/workplace/total',
    method: 'get',
    timeout,
    response: () => {
      return {
        code: result_code,
        data: {
          project: 40,
          access: 2340,
          todo: 10
        }
      }
    }
  },
  // 获取项目
  {
    url: '/api/workplace/project',
    method: 'get',
    timeout,
    response: () => {
      return {
        code: result_code,
        data: [
          {
            name: 'Github',
            icon: 'akar-icons:github-fill',
            message: 'workplace.introduction',
            personal: 'kinit',
            time: new Date()
          },
          {
            name: 'Vue',
            icon: 'logos:vue',
            message: 'workplace.introduction',
            personal: 'kinit',
            time: new Date()
          },
          {
            name: 'Angular',
            icon: 'logos:angular-icon',
            message: 'workplace.introduction',
            personal: 'kinit',
            time: new Date()
          },
          {
            name: 'React',
            icon: 'logos:react',
            message: 'workplace.introduction',
            personal: 'kinit',
            time: new Date()
          },
          {
            name: 'Webpack',
            icon: 'logos:webpack',
            message: 'workplace.introduction',
            personal: 'kinit',
            time: new Date()
          },
          {
            name: 'Vite',
            icon: 'vscode-icons:file-type-vite',
            message: 'workplace.introduction',
            personal: 'kinit',
            time: new Date()
          }
        ]
      }
    }
  },
  // 获取动态
  {
    url: '/api/workplace/dynamic',
    method: 'get',
    timeout,
    response: () => {
      return {
        code: result_code,
        data: [
          {
            keys: ['workplace.push', 'Github'],
            time: new Date()
          },
          {
            keys: ['workplace.push', 'Github'],
            time: new Date()
          }
        ]
      }
    }
  },
  // 获取团队信息
  {
    url: '/api/workplace/team',
    method: 'get',
    timeout,
    response: () => {
      return {
        code: result_code,
        data: [
          {
            name: 'Github',
            icon: 'akar-icons:github-fill'
          },
          {
            name: 'Vue',
            icon: 'logos:vue'
          },
          {
            name: 'Angular',
            icon: 'logos:angular-icon'
          },
          {
            name: 'React',
            icon: 'logos:react'
          },
          {
            name: 'Webpack',
            icon: 'logos:webpack'
          },
          {
            name: 'Vite',
            icon: 'vscode-icons:file-type-vite'
          }
        ]
      }
    }
  }
] as MockMethod[]
