from socket import *
import os, os.path
import time

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43211
MIDDLEWARE_PORT = 43210
BACKUP_PORT = 43212
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

def backup(filename):
    """
    Função para execução do backup do arquivo em outro server
    """

    # Criando socket TCP
    sock = socket(AF_INET, SOCK_STREAM)

    # Conectando ao servidor
    sock.connect((IP_ADDRESS, BACKUP_PORT))

    # Acessando arquivo
    if ".txt" or ".pdf" in filename:
        file = open(filename, "rb")

        # Armazenando dados do arquivo
        data = file.read()

        flag = 2
        # Enviando flag ao servidor
        print(f"Enviando flag ao servidor.... {flag}")
        sock.sendall(str(flag).encode())

        time.sleep(2)

        # Enviando nome do arquivo ao servidor
        print(f"Enviando nome do arquivo.... {filename}")
        sock.sendall(filename.encode())

        time.sleep(3)

        # Enviando arquivo ao servidor
        print(f"Enviando arquivo....")
        sock.sendall(data)

        print("Arquivo enviado...")

        file.close()

    elif ".png" or ".jpeg" or ".jpg" in filename:
        with open(filename, "rb") as file:

            # Armazenando dados do arquivo
            data = file.read(BUFFER_SIZE)

            flag = 2
            # Enviando flag ao servidor
            print(f"Enviando flag ao servidor.... {flag}")
            sock.sendall(str(flag).encode())

            time.sleep(2)

            # Enviando nome do arquivo ao servidor
            print("Enviando nome do arquivo....")
            sock.send(filename.encode())

            time.sleep(3)

            while data:
                # Enviando arquivo ao servidor
                print("Enviando arquivo....")
                sock.send(data)
                data = file.read(BUFFER_SIZE)

        print("Arquivo enviado...")

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

    # Recebendo flag de envio
    flag = conn.recv(BUFFER_SIZE).decode()
    flag = int(flag)
    print(f"Recebendo flag de envio: {flag}...")

    # Recebendo nome do arquivo
    filename = conn.recv(BUFFER_SIZE).decode()
    print(f"Recebendo nome do arquivo: {filename}...")

    # Recebendo dados do arquivo
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

    # Executa backup no outro servidor
    if flag == 1:
        backup(filename)

if __name__ == '__main__':
    send_file_storage_to_middleware(IP_ADDRESS, MIDDLEWARE_PORT)

    start_server(IP_ADDRESS, PORT, BUFFER_SIZE)