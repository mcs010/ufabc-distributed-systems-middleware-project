from socket import *
import os

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43210
BUFFER_SIZE = 1024

# Iniciando socket TCP
server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind((IP_ADDRESS, PORT))

# Servidor esperando conexão do client
server_socket.listen()
print("Servidor aguardando conexao....")

while True:
    # Servidor aceita conexao do client
    conn, addr = server_socket.accept()
    print(f"Conectado ao client {conn}/{addr}")

    # Recebendo nome do arquivo
    filename = conn.recv(BUFFER_SIZE).decode('utf-8')
    print(f"Recebendo nome do arquivo: {filename}")
    
    if ".txt" in filename:
        file = open(filename, "w")
        print(f"Nome do arquivo recebido")

        # Recebendo dados do arquivo do client
        print("Recebendo dados do arquivo....")
        data = conn.recv(BUFFER_SIZE).decode()
        file.write(data)
        print("Arquivo recebido")

        file.close()

        conn.close()

    elif ".png" in filename:
        with open(filename, "wb") as file:
            received_data = conn.recv(BUFFER_SIZE)

            while data:
                file.write(received_data)
                received_data = conn.recv(BUFFER_SIZE)

            print("Arquivo recebido......")

obj_socket = socket(AF_INET, SOCK_STREAM)

# Conectando ao requerente da conexao
obj_socket.bind((client_address, port))
obj_socket.listen(2) # Qtd max de clientes que a aplicação irá escutar/receber conexão

print("Servidor iniciado!!!")
print("Aguardando cliente...")

conn, client = obj_socket.accept()
print("Conectado com: ", client)

# Armazenando arquivo no servidor
filename = conn.recv(TRANSFER_SIZE).decode()
print("Nome arquivo: ", filename)

# Recebendo arquivo
data = conn.recv(TRANSFER_SIZE).decode()

# Cria arquivo no servidor recebendo o nome do arquivo pelo 'filename'
open_file = open(filename, 'w')

print("Recebendo arquivo")
while data:
    open_file.write(data)
    #data = conn.recv(TRANSFER_SIZE).decode()

    if not data:
        break

print(f"Arquivo {filename} recebido!!!")

open_file.close()

# Fecha a conexao
conn.close()