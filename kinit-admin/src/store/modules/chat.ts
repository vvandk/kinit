import { defineStore } from 'pinia'
import { store } from '../index'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

interface ChatState {
  socket: any
  messageQueue: string[]
  socketMessage: string
}

export const useChatStore = defineStore('chat', {
  state: (): ChatState => {
    return {
      socket: null,
      messageQueue: [],
      socketMessage: '1'
    }
  },
  getters: {},
  actions: {
    SET_SOCKET(socket: any) {
      this.socket = socket
    },
    SET_SOCKET_MESSAGE(socketMessage: any) {
      this.socketMessage = socketMessage
    },
    connectWebSocket() {
      if (typeof WebSocket === 'undefined') {
        ElMessage.error('您的浏览器不支持Websocket通信协议，请使用Chrome或者其他高版本的浏览器！')
        return
      }
      if (this.socket != null && this.socket.readyState === WebSocket.OPEN) {
        return this.socket
      }

      const HOST_ADDRESS = 'ws://127.0.0.1:8000/api/v1/ws/chat/'
      const PING_INTERVAL = 5000 // 心跳间隔，单位为毫秒
      const heartbeatMessage = { type: 0, msg: 'ping' } // 心跳消息
      const heartbeatMessage2 = { type: 0, msg: 'pong', data: ['在线设备'] } // 发送消息

      const socket = ref<WebSocket>(new WebSocket(HOST_ADDRESS))
      let checkTask: any = null
      // 监听连接事件
      socket.value.onopen = () => {
        // 启动心跳检测 确保连接存活 客户端每隔5秒向服务端发送一次心跳消息
        checkTask = setInterval(() => {
          socket.value.send(JSON.stringify(heartbeatMessage))
        }, PING_INTERVAL)
      }

      // 当WebSocket接收到服务器发送的消息时，这个函数将被调用。
      socket.value.onmessage = (event) => {
        console.log('接收到服务端发送过来的消息', event.data)
        const message = JSON.parse(event.data)
        console.log(message.type)
        if (message.type == WebSocket.CONNECTING) {
          socket.value.send(JSON.stringify(heartbeatMessage2))
          return
        } else {
          if (this.messageQueue.length > 2 << 16) {
            this.messageQueue = []
          }
          console.log('WebSocket消息: ', message)
          this.SET_SOCKET_MESSAGE(message)
        }
      }

      // 监听关闭事件 断线重连
      socket.value.onclose = () => {
        if (this.socket.readyState === WebSocket.CLOSED) {
          this.messageQueue.forEach((message) => {
            this.sendMessage(message)
          })
          this.messageQueue = []
        }
        // 清除心跳计时器
        checkTask && clearInterval(checkTask)
        // 断线重连
        setTimeout(() => {
          this.connectWebSocket()
        }, 3000)
      }

      // 连接错误
      socket.value.onerror = (event) => {
        console.log('WebSocket error:', event)
      }
    },
    // 发送消息方法
    sendMessage(message: string) {
      this.socket.send(message)
    }
  },
  persist: true
})

export const useChatStoreWithOut = () => {
  return useChatStore(store)
}
