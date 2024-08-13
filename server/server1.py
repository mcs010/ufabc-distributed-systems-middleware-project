from socket import *
import os, os.path

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43211
MIDDLEWARE_PORT = 43210
BUFFER_SIZE = 4096

def get_size_files_dir_path():
    """
    Função para calcular tamanho total dos arquivos armazenados no diretorio atual
    Retorna o tamanho total
    """
    directory_path = os.getcwd()
    files = list(os.listdir(directory_path))

    total_size = 0
    for file in files:
        stat = os.stat(file)
        total_size = total_size + stat.st_size

    return total_size

def send_file_storage_to_middleware(IP_ADDRESS, MIDD_PORT):
    
    # Criando socket TCP
    sock = socket(AF_INET, SOCK_STREAM)

    # Conectando ao middleware
    sock.connect((IP_ADDRESS, MIDD_PORT))

    # Total de tamanho ocupado no diretorio atual
    storage = get_size_files_dir_path()

    # Enviando tamanho do diretorio ao middleware
    sock.sendall(str(storage).encode())

    sock.close()


def start_server(IP_ADDRESS, PORT, BUFFER_SIZE):
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

if __name__ == '__main__':
    send_file_storage_to_middleware(IP_ADDRESS, MIDDLEWARE_PORT)

    start_server(IP_ADDRESS, PORT, BUFFER_SIZE)