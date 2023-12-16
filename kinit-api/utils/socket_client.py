import json
import socket


class SocketClient:
    """
    socket 客户端操作
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 3636):
        """
        :param host:
        :param port:
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    def udp_send_message(self, message: str):
        """
        发送消息
        :param message:
        :return:
        """
        # 如果你想接收响应
        self.client_socket.sendto(message.encode('utf-8'), (self.host, self.port))

    def close(self):
        """
        关闭 socket 连接
        :return:
        """
        self.client_socket.close()


if __name__ == '__main__':
    SC = SocketClient()
    SC.udp_send_message(json.dumps({"training_id": 1, "instruct": "4"}))
    SC.close()
