from socket import *
import os

client_address = "127.0.0.1" #localhost
port = 43210

TRANSFER_SIZE = 1024

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