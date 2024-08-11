from socket import *
import os

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43211
BUFFER_SIZE = 1024

# Iniciando socket TCP
server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind((IP_ADDRESS, PORT))

# Servidor esperando conexão do client
server_socket.listen()
print("Servidor aguardando conexao....")

# Servidor aceita conexao do client
conn, addr = server_socket.accept()
print(f"Conectado ao client {conn}/{addr}")

# Recebendo nome do arquivo
filename = conn.recv(BUFFER_SIZE).decode()
print(f"Recebendo nome do arquivo: {filename}...")

# Recebendo dados do arquivo
process_finished = False

file_bytes = b""

while True:
    file_data = conn.recv(BUFFER_SIZE)

    if not file_data:
        break
    
    file_bytes += file_data

with open(filename, "wb") as file:
    file.write(file_bytes)

print(f"Arquivo {filename} recebido")

server_socket.close()