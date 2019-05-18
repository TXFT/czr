from socket import *
import pandas as pd



def main():
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.connect(("127.0.0.1", 8888))
    print(tcpSocket.recv(1024).decode("utf-8"))
    for data in [b"Orystal0", b"Orystal1", b"Orystal2"]:
        tcpSocket.send(data)
        print(tcpSocket.recv(1024).decode("utf-8"))
    tcpSocket.send(b"exit")
    tcpSocket.close()


if __name__ == '__main__':
    main()