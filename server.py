from socket import *
from threading import *
import time


def tcplink(sock, addr):
    print("接收到一个来自%s:%s的连接请求" % addr)
    sock.send(b"welcome!\n")
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode("utf-8") == "exit":
            break
        sock.send(("hello,%s" % data.decode("utf-8")).encode())
    sock.close()
    print("来自%s:%s的连接关闭！" % addr)


def main():
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.bind(("127.0.0.1", 8888))
    tcpSocket.listen(5)
    print("等待客户端连接...")
    while True:
        sock, addr = tcpSocket.accept()
        t = Thread(target=tcplink, args=(sock, addr))
        t.start()


if __name__ == '__main__':
    main()