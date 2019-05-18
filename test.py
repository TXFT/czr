import socket


# 建立tcp socket 建立和Http服务器的tcp连接
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(('127.0.0.1', 80))
# 拼接HTTP请求报文
"""
GET / HTTP/1.1\r\n
Host:itcastcpp.cn\r\n
\r\n
"""
request_line = "GET / HTTP/1.1\r\n"
request_header = "Host:itcastcpp.cn\r\n"
request_data = request_line + request_header + "\r\n"
# 发送
tcp_socket.send(request_data.encode())
# 收数据
recv_data = tcp_socket.recv(4096)
print(recv_data.decode())
# 关闭连接
tcp_socket.close()
