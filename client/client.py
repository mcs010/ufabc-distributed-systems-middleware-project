from socket import *
import os

# Address and port
server = "127.0.0.1"
port = 43210
transfer_size = 1024
size_status = 0

filename = input("Digite o nome do arquivo: ")
file_size = os.path.getsize(filename)

file = open(filename, "rb")

obj_socket = socket(AF_INET, SOCK_STREAM)

# Conecta ao host
obj_socket.connect((server, port))

while True:
    try:
        data = file.read(transfer_size) 
        while data:
            print("Enviando arquivo...")
            obj_socket.sendall(data)
            data = file.read(transfer_size)
            size_status += transfer_size
            print(f"Enviando {size_status}/{file_size}")
        file.close()
        break
    except:
        print("Erro ao enviar o arquivo!!!")

obj_socket.send(b"Enviado...")

print("ARQUIVO ENVIADO")
print(obj_socket.recv(transfer_size))

obj_socket.shutdown(2)

# Fechar conexão
obj_socket.close()