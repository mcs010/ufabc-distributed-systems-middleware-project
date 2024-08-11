from socket import *
import time
#from ..client.client import get_filename_buffer

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43210
PORT_2 = 43211
BUFFER_SIZE = 1024
#FILENAME_BUFFER = get_filename_buffer()

def connect_to_client(IP_ADDRESS, PORT):
    """
    Funçao para conectar cliente ao middleware
    Retorna o socket object
    """
    # Iniciando socket TCP
    middleware_socket = socket(AF_INET, SOCK_STREAM)

    middleware_socket.bind((IP_ADDRESS, PORT))

    return middleware_socket
    

def receive_from_client(IP_ADDRESS, PORT):
    """
    Receives file from client socket
    """
    # Inicia conexao
    middleware_socket = connect_to_client(IP_ADDRESS, PORT)

    # Middleware esperando conexão do client
    middleware_socket.listen()
    print("Gerenciador aguardando conexao....")

    # Middleware aceita conexao do client
    conn, addr = middleware_socket.accept()
    print(f"Conectado ao client {conn}/{addr}")

    filename = conn.recv(BUFFER_SIZE).decode()
    print(f"Nome recebido: {filename}")

    #process_finished = False

    file_bytes = b""

    while True:
        file_data = conn.recv(BUFFER_SIZE)

        if not file_data:
            break
        
        file_bytes += file_data

    return filename, file_bytes

def connect_to_server(IP_ADDRESS, PORT_2):
    """
    Funçao para conectar middleware ao servidor
    Retorna o socket object
    """
    # Criando socket TCP
    middleware_socket = socket(AF_INET, SOCK_STREAM)

    # Conectando ao servidor
    middleware_socket.connect((IP_ADDRESS, PORT_2))

    return middleware_socket

def send_to_server(IP_ADDRESS, PORT_2, filename, file_data):
    """
    Sends file to server socket
    """

    socket = connect_to_server(IP_ADDRESS, PORT_2)

    # Enviando nome do arquivo ao servidor
    print(f"Enviando nome do arquivo.... {filename}")
    socket.sendall(filename.encode())

    time.sleep(3)

    # Enviando arquivo ao servidor
    print(f"Enviando arquivo....")
    socket.sendall(file_data)

    print("Arquivo enviado...")

    socket.close()

if __name__ == '__main__':

    filename, file_data = receive_from_client(IP_ADDRESS, PORT)

    send_to_server(IP_ADDRESS, PORT_2, filename, file_data)