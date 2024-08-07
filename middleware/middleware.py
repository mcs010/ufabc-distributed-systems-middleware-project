from socket import *

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43210
PORT_2 = 43211
BUFFER_SIZE = 1024

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

    while True:
        # Middleware aceita conexao do client
        conn, addr = middleware_socket.accept()
        print(f"Conectado ao client {conn}/{addr}")

        # Recebendo nome do arquivo
        filename = conn.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Recebendo nome do arquivo: {filename}")
        
        if ".txt" in filename:
            print(f"Nome do arquivo recebido")

            # Recebendo dados do arquivo do client
            print("Recebendo dados do arquivo....")
            data = conn.recv(BUFFER_SIZE).decode()
            #file.write(data)
            print("Arquivo recebido")

            #file.close()

            return filename, data

        elif ".png" in filename:
            received_data = conn.recv(BUFFER_SIZE)

            while received_data:
                received_data = conn.recv(BUFFER_SIZE)

            print("Arquivo recebido......")

            return filename, data
        
        conn.close()


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

def send_to_server(IP_ADDRESS, PORT_2, filename, filedata):
    """
    Sends file to server socket
    """

    socket = connect_to_server(IP_ADDRESS, PORT_2)

    # Acessando arquivo
    if ".txt" in filename:

        # Armazenando dados do arquivo
        data = filedata

        # Enviando nome do arquivo ao servidor
        print("Enviando nome do arquivo....")
        socket.send(filename.encode('utf-8'))

        # Enviando arquivo ao servidor
        print("Enviando arquivo....")
        socket.sendall(data.encode())

    elif ".png" in filename:
            # Armazenando dados do arquivo
            data = filedata.read(BUFFER_SIZE)

            # Enviando nome do arquivo ao servidor
            print("Enviando nome do arquivo....")
            socket.send(filename.encode('utf-8'))

            while data:
                # Enviando arquivo ao servidor
                print("Enviando arquivo....")
                socket.send(data)
                data = filedata.read(BUFFER_SIZE)

    socket.close()

if __name__ == '__main__':

    filename, filedata = receive_from_client(IP_ADDRESS, PORT)

    send_to_server(IP_ADDRESS, PORT_2, filename, filedata)