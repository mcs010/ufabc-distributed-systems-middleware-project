from socket import *
import os

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43210
BUFFER_SIZE = 1024
FILENAME = input("Digite o nome do arquivo: ")
print("Nome arquivo: ", FILENAME)

# Criando socket TCP
client_socket = socket(AF_INET, SOCK_STREAM)

# Conectando ao servidor
client_socket.connect((IP_ADDRESS, PORT))

# Acessando arquivo
if ".txt" in FILENAME:
    file = open(FILENAME, "r")

    # Armazenando dados do arquivo
    data = file.read()

    # Enviando nome do arquivo ao servidor
    print("Enviando nome do arquivo....")
    client_socket.send(FILENAME.encode('utf-8'))

    # Enviando arquivo ao servidor
    print("Enviando arquivo....")
    client_socket.sendall(data.encode())

    file.close()

elif ".png" in FILENAME:
    with open(FILENAME, "rb") as file:

        # Armazenando dados do arquivo
        data = file.read(BUFFER_SIZE)

        # Enviando nome do arquivo ao servidor
        print("Enviando nome do arquivo....")
        client_socket.send(FILENAME.encode('utf-8'))

        while data:
            # Enviando arquivo ao servidor
            print("Enviando arquivo....")
            client_socket.send(data)
            data = file.read(BUFFER_SIZE)

client_socket.close()