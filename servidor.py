import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('localhost', 3333))

s.listen(5)
flag = 0
while True:
    connect, addr = s.accept()
    print("Connection Address:" + str(addr))

    str_return = "Welcome to visit my test socket server. Waiting for command."
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_recv, temp = connect.recvfrom(1024)
    print(str_recv)

    str_return = "I got your command, it is " + str(str_recv)
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    connect.close()