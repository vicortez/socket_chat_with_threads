import socket
import threading
import time
import os


def accept_client():
    global CONNECTION_LIST
    while True:
        client_socket, client_address = server_socket.accept()
        username = client_socket.recv(1024)
        print('%s is now connected' % username.decode("UTF-8"))
        msg = bytes(str(username.decode("UTF-8") + " is now connected"), encoding="UTF-8")
        broadcast_message(client_socket, username, client_address, msg)
        CONNECTION_LIST.append((username, client_socket, client_address))
        thread_client = threading.Thread(target=client_connection, args=[username, client_socket, client_address])
        thread_client.start()


def flood_prevention(list):
    if len(list)>=5:
        print(list)
        last = list[len(list)-1]
        first = list[len(list)-5]
        dif = last - first
        print(dif)
        if dif>2:
            return True
        else:
            return False
    return True


def client_connection(username, client_socket, client_address):
    global CONNECTION_LIST
    msgTimeList=[]
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                current_time=lambda: int(round(time.time()))
                msgTimeList.append(current_time())
                if flood_prevention(msgTimeList):
                    comando = data.decode("UTF-8")
                    if comando == "sair()":
                        sair(client_socket, username, client_address)
                    # listarServ()
                    elif comando == "listar()":
                        msg = "\nUsers List: \n"
                        for client in CONNECTION_LIST:
                            msg += "nome: " + client[0].decode("UTF-8") + ", IP: " + client[2][0] + ", PORT: " + str(
                                client[2][1]) + "\n"
                        client_socket.send(bytes(msg, encoding="UTF-8"))
                    elif comando[0:5] == "nome(" and comando[-1] == ")":
                        newName = comando[5:-1]
                        msg = bytes(str(username.decode("UTF-8") + " changed nickname to " + newName), encoding="UTF-8")
                        for client in CONNECTION_LIST:
                            if client == (username, client_socket, client_address):
                                print(client[0].decode("UTF-8"), "changed nickname to", newName)
                                CONNECTION_LIST.remove(client)
                                username = bytes(newName, encoding="UTF-8")
                                CONNECTION_LIST.append((username, client_socket, client_address))
                                # listarServ()
                                break
                        broadcast_message(client_socket, username, client_address, msg)
                    else:
                        print(username.decode("UTF-8") + " spoke: " + data.decode("UTF-8"))
                        msg = bytes(str(username.decode("UTF-8") + " spoke:  " + data.decode("UTF-8")), encoding="UTF-8")
                        broadcast_message(client_socket, username, client_address, msg)
                else:
                    client_socket.send(bytes("NO SPAM PLS", encoding="UTF-8"))
                    time.sleep(10)
        except Exception as x:
            # print(x)
            # sair(client_socket, username,client_address)
            # listarServ()
            # msg=bytes(str(username.decode("UTF-8")+ " disconnected"),encoding="UTF-8")
            # broadcast_message(client_socket, username,client_address, msg)
            break


def broadcast_message(cs_sock, sen_name, client_address, msg):
    global CONNECTION_LIST
    for client in CONNECTION_LIST:
        client[1].send(msg)


def comando():
    global CONNECTION_LIST
    while True:
        msg = input()
        if msg == "listar()":
            listarServ()
        elif msg == "sair()":
            for client in CONNECTION_LIST:
                print(client[0].decode("UTF-8") + " disconnected")
                msg = bytes(str(client[0].decode("UTF-8") + " disconnected"), encoding="UTF-8")
                client[1].send(bytes("s2_close_s2", encoding="UTF-8"))
                time.sleep(1)
                client[1].close()
            # CONNECTION_LIST.remove(client)
            # broadcast_message(client[1], client[0],client[2], msg)
            os._exit(0)


def sair(client_socket, username, client_address):
    global CONNECTION_LIST
    for client in CONNECTION_LIST:
        if client == (username, client_socket, client_address):
            print(client[0].decode("UTF-8") + " disconnected2")
            msg = bytes(str(client[0].decode("UTF-8") + " disconnected 2"), encoding="UTF-8")
            client[1].send(bytes("s2_close_s2", encoding="UTF-8"))
            client[1].close()
            CONNECTION_LIST.remove(client)
            broadcast_message(client[1], client[0], client[2], msg)
            break


def listarServ():
    print("\nUsers List: \n")
    global CONNECTION_LIST
    for client in CONNECTION_LIST:
        print("nome: " + client[0].decode("UTF-8") + ", IP: " + client[2][0] + ", PORT: " + str(client[2][1]))


CONNECTION_LIST = []
HOST = ''
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)
print('Chat server started on port : ' + str(PORT))

thread_accept = threading.Thread(target=accept_client)
thread_accept.start()

thread_comando = threading.Thread(target=comando)
thread_comando.start()
