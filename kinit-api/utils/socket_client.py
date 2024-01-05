import json
import socket


class SocketClient:
    """
    socket 客户端操作
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 3636, send_type: str = "tcp"):
        """
        :param host: socket server 地址
        :param port: socket server 端口
        :param send_type: 通信协议
        """
        self.send_type = send_type
        if self.send_type == "tcp":
            socket_type = socket.SOCK_STREAM
        elif self.send_type == "udp":
            socket_type = socket.SOCK_DGRAM
        else:
            print("不支持通信协议")
            raise ValueError("不支持的通信协议")
        self.client_socket = socket.socket(socket.AF_INET, socket_type)
        self.host = host
        self.port = port
        if self.send_type == "tcp":
            self.tcp_connect()

    def tcp_connect(self):
        """
        TCP 连接服务端
        :return:
        """
        self.client_socket.connect((self.host, self.port))
        print("tcp 连接成功")

    def udp_send_message(self, message: str):
        """
        UDP 发送消息
        :param message:
        :return:
        """
        self.client_socket.sendto(message.encode('utf-8'), (self.host, self.port))
        print("udp 消息发送成功：", message)

    def tcp_send_message(self, message: str):
        """
        TCP 发送消息
        :param message:
        :return:
        """
        self.client_socket.sendall(message.encode('utf-8'))
        print("tcp 消息发送成功：", message)

    def send_message(self, message: str):
        """
        TCP 发送消息
        :param message:
        :return:
        """
        if self.send_type == "tcp":
            self.tcp_send_message(message)
        elif self.send_type == "udp":
            self.udp_send_message(message)
        else:
            print("不支持协议")
            raise ValueError("不支持的协议")

    def close(self):
        """
        关闭 socket 连接
        :return:
        """
        self.client_socket.close()


if __name__ == '__main__':
    _host = "127.0.0.1"
    _port = 3636

    SC = SocketClient()
    SC.tcp_send_message(json.dumps({"label": "ceshi", "value": 1}))
    SC.close()
