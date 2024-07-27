from socket import *
import os
import time
#
# Address and port
server = "127.0.0.1"
port = 43210
TRANSFER_SIZE = 1024
size_status = 0

filename = input("Digite o nome do arquivo: ")
print("Nome arquivo: ", filename)
file_size = os.path.getsize(filename)

obj_socket = socket(AF_INET, SOCK_STREAM)

# Conecta ao host
obj_socket.connect((server, port))

with open(filename, "rb") as file:
    while True:
        obj_socket.sendall(filename.encode())
        time.sleep(2)
        data = file.read()
        print(f"Enviando arquivo {filename}")
        obj_socket.sendall(data)
        if not data:
            print('Saindo do envio')
            break

print("ARQUIVO ENVIADO")
#print(obj_socket.recv(TRANSFER_SIZE))

obj_socket.shutdown(2)

# Fechar conexão
obj_socket.close()