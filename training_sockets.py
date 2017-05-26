# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP (python 3)
#

# importacao das bibliotecas
import socket
import os.path  # serve para usar a funcao os.path.isfile('nome do arquivo')

# definicao do host e da porta do servidor
HOST = ''  # ip do servidor (em branco)
PORT = 8080  # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# mantem o socket ativo mesmo apos a conexao ser encerrada (faz o reuso do endereco do servidor)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)

# vincula o socket com a porta (faz o "bind" do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(5)

# imprime que o servidor esta pronto para receber conexoes
print("Serving HTTP on port %s ..." % PORT)

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    print("connected to client socket:",client_address)
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    # ex.: GET /TesteHTML.html HTTP/1.1
    pedidoGET = request.split(b' ')  # retorna o vetor dividido

    if (pedidoGET[0] == b'GET'):
        caminho = pedidoGET[1].split(b'/')[1]
        if (caminho == b'' or caminho==b'\r\n'):  # caminho vazio retornar index.html
            caminho = b'index.html'
        if (os.path.isfile(caminho)):

            arquivo = open(caminho, 'rb')
            # declaracao da resposta do servidor
            http_response = b"""\HTTP/1.1 200 OK \r\n\r\n"""
            client_connection.send(http_response)

            leitura = arquivo.readlines()  # retorna lista de str onde cada str é uma linha
            for i in range(0, len(leitura)):  # enviar linha a linha do arquivo
                http_response = leitura[i]
                client_connection.send(http_response)

            client_connection.send(b"\r\n")
        else:
            # Not Found
            http_response = b"""\
HTTP/1.1 404 Not Found \r\n\r\n
<html><head></head><body><h1>404 Not Found </h1></body></html>\r\n"""
            client_connection.send(http_response)

    else:
        # Bab Request
        print("noBaby")
        http_response = b"""\
HTTP/1.1 400 Bad Request \r\n\r\n
<html><head></head><body><h1>400 Bad Request </h1></body></html>\r\n"""
        client_connection.send(http_response)

    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    # client_connection.send(http_response)
    # encerra a conexao
    client_connection.close()
