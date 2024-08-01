from socket import *

# Address and port
IP_ADDRESS = "127.0.0.1"
PORT = 43210
BUFFER_SIZE = 1024

def connect_to_client():
    """
    Funçao para conectar cliente ao middleware
    Retorna o socket object
    """

def receive_from_client(IP_ADDRESS, PORT):
    """
    Receives file from client socket
    """
    # Criando socket TCP
    middleware_socket = socket(AF_INET, SOCK_STREAM)

    # Conectando ao servidor
    middleware_socket.connect((IP_ADDRESS, PORT))

def connect_to_server(IP_ADDRESS, PORT):
    """
    Funçao para conectar middleware ao servidor
    Retorna o socket object
    """
    # Criando socket TCP
    middleware_socket = socket(AF_INET, SOCK_STREAM)

    # Conectando ao servidor
    middleware_socket.connect((IP_ADDRESS, PORT))

    return middleware_socket

def send_to_server():
    """
    Sends file to server socket
    """