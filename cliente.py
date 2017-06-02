import socket, threading, time
import os


def send():
    global is_a_spammer
    while True:
        try:
            msg = input()
            if not is_a_spammer:
                cli_sock.send(bytes(msg, encoding="UTF-8"))
        except:
            break


def receive():
    global is_a_spammer
    while True:
        data = cli_sock.recv(1024)
        print(str(data.decode("UTF-8")))
        if data.decode("UTF-8") == "NO SPAM PLS":
            is_a_spammer = True
            time.sleep(10)
            is_a_spammer = False
        if data.decode("UTF-8") == "s2_close_s2":
            print("Servidor mandou encerrar")
            cli_sock.close()
            os._exit(0)


if __name__ == "__main__":
    is_a_spammer=False
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 9999
    cli_sock.connect((HOST, PORT))
    print('Connected to remote host...')
    uname = input('Enter your name to enter the chat > ')
    cli_sock.send(bytes(uname, encoding="UTF-8"))

    thread_send = threading.Thread(target=send)
    thread_send.start()

    thread_receive = threading.Thread(target=receive)
    thread_receive.start()
