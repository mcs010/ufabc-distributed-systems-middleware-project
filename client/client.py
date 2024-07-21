from socket import *

# Address and port
server = "127.0.0.1"
port = 43210

filepath = input("Digite o caminho do arquivo: ")

file = open(filepath, "rb")

data = file.read(1024)

obj_socket = socket(AF_INET, SOCK_STREAM)

while data:
    print("Enviando arquivo...")
    obj_socket.sendall(data)
    data = file.read(1024)

file.close()

obj_socket.send(b"Enviado...")

print("ARQUIVO ENVIADO")
print(obj_socket.recv(1024))

obj_socket.shutdown(2)
obj_socket.close()