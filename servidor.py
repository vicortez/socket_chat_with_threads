import socket
import threading

def accept_client():
    while True:
        client_socket, client_address = server_socket.accept()
        username = client_socket.recv(1024)
        CONNECTION_LIST.append((username, client_socket))
        print('%s is now connected' %username)
        thread_client = threading.Thread(target = client_connection, args=[username, client_socket])
        thread_client.start()

def client_connection(username, client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                print (format(username),"spoke:",data)
                broadcast_message(client_socket, username, data)
        except Exception as x:
            print(x.message)
            break

def broadcast_message(cs_sock, sen_name, msg):
    for client in CONNECTION_LIST:
        #if client[1] != cs_sock:
        client[1].send(sen_name + b': ' + msg)
        #client[1].send(msg)

CONNECTION_LIST=[]
HOST = ''
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)
print('Chat server started on port : ' + str(PORT))

thread_accept = threading.Thread(target=accept_client)
thread_accept.start()

