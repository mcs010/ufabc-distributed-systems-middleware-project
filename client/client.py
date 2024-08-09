from socket import *
import sys, os, time

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43210
BUFFER_SIZE = 1024
FILENAME = input("Digite o nome do arquivo: ")
FILESIZE = os.path.getsize(FILENAME)
print("Nome arquivo: ", FILENAME)

# Criando socket TCP
client_socket = socket(AF_INET, SOCK_STREAM)

# Conectando ao servidor
client_socket.connect((IP_ADDRESS, PORT))

# Acessando arquivo
if ".txt" in FILENAME:
    file = open(FILENAME, "rb")

    # Armazenando dados do arquivo
    data = file.read()

    # Enviando nome do arquivo ao servidor
    print(f"Enviando nome do arquivo.... {FILENAME}")
    client_socket.sendall(FILENAME.encode())

    time.sleep(3)

    # Enviando arquivo ao servidor
    print(f"Enviando arquivo.... {data}")
    client_socket.sendall(data)

    print("Arquivo enviado...")

    file.close()

elif ".png" in FILENAME:
    with open(FILENAME, "rb") as file:

        # Armazenando dados do arquivo
        data = file.read(BUFFER_SIZE)

        # Enviando nome do arquivo ao servidor
        print("Enviando nome do arquivo....")
        client_socket.send(FILENAME.encode())

        time.sleep(3)

        while data:
            # Enviando arquivo ao servidor
            print("Enviando arquivo....")
            client_socket.send(data)
            data = file.read(BUFFER_SIZE)

    print("Arquivo enviado...")

client_socket.close()