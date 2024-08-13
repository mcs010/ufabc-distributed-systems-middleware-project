from socket import *
import time
import threading
import concurrent.futures
import numpy as np

# Address and port
IP_ADDRESS = "127.0.0.1"
MIDDLEWARE_PORT = 43210
MIDDLEWARE_PORT_2 = 43215
PORT_2 = 43211
PORT_3 = 43212
BUFFER_SIZE = 4096
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

    file_bytes = b""

    while True:
        file_data = conn.recv(BUFFER_SIZE)

        if not file_data:
            break
        
        file_bytes += file_data

    return filename, file_bytes

def connect_to_server(IP_ADDRESS, PORT):
    """
    Funçao para conectar middleware ao servidor
    Retorna o socket object
    """
    # Criando socket TCP
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Conectando ao servidor
    server_socket.connect((IP_ADDRESS, PORT))

    return server_socket

def send_to_server(IP_ADDRESS, PORT, filename, file_data):
    """
    Sends file to server socket
    """

    socket = connect_to_server(IP_ADDRESS, PORT)

    # Enviando nome do arquivo ao servidor
    print(f"Enviando nome do arquivo.... {filename}")
    socket.sendall(filename.encode())

    time.sleep(3)

    # Enviando arquivo ao servidor
    print(f"Enviando arquivo....")
    socket.sendall(file_data)

    print("Arquivo enviado...")

    socket.close()

def get_server_storage_of_files(connection):
    """
    Função para obter numero de arquivos um servidor
    Retorna o numero de arquivos
    """

    server_response = connection.recv(BUFFER_SIZE).decode()

    return server_response

def get_less_loaded_server(result_list):

    return sorted(result_list, key=lambda tup: tup[1])

if __name__ == '__main__':

    # Iniciando socket TCP
    middleware_socket = socket(AF_INET, SOCK_STREAM)

    middleware_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    middleware_socket.bind((IP_ADDRESS, MIDDLEWARE_PORT))

    # Middleware esperando conexão do client
    middleware_socket.listen(2)
    print("Middleware aguardando conexao....")

    chosen_server = []
    for i in range(3):
        conn, address = middleware_socket.accept()

        with concurrent.futures.ThreadPoolExecutor(2) as executor:
            futures = [executor.submit(get_server_storage_of_files, conn)]

            return_values = [future.result() for future in futures]

        chosen_server.append(int(return_values[0]))
        print(chosen_server)

        
    print(np.argmin(chosen_server))
    server_index = np.argmin(chosen_server)

    if server_index == 0:
        port = PORT_2
    elif server_index == 1:
        port = PORT_3

    middleware_socket.close()
    
    # Recebe arquivo do client
    filename, file_data = receive_from_client(IP_ADDRESS, MIDDLEWARE_PORT_2)

    # Envia arquivo ao server escolhido
    send_to_server(IP_ADDRESS, port, filename, file_data)