from socket import *
import sys, os, time

def client_menu():
    """
    Função para o menu do client
    Retorna um valor de controle do fluxo: 1 - envia arquivo e 2 fecha o programa
    """
    print("Escolha uma opção:")
    print("1 - Backup de arquivo")
    print("2 - Sair")

    choice = int(input())

    return choice

def sending_file():
    # Address and port
    IP_ADDRESS = "127.0.0.1"
    PORT = 43210
    BUFFER_SIZE = 1024
    FILENAME = input("Digite o nome do arquivo: ")
    FILESIZE = os.path.getsize(FILENAME)
    print("Nome arquivo: ", FILENAME)

    # Criando socket TCP
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Conectando ao servidor
    client_socket.connect((IP_ADDRESS, PORT))

    # Acessando arquivo
    if ".txt" or ".pdf" in FILENAME:
        file = open(FILENAME, "rb")

        # Armazenando dados do arquivo
        data = file.read()

        # Enviando nome do arquivo ao servidor
        print(f"Enviando nome do arquivo.... {FILENAME}")
        client_socket.sendall(FILENAME.encode())

        time.sleep(3)

        # Enviando arquivo ao servidor
        print(f"Enviando arquivo....")
        client_socket.sendall(data)

        print("Arquivo enviado...")

        file.close()

    elif ".png" or ".jpeg" or ".jpg" in FILENAME:
        with open(FILENAME, "rb") as file:

            # Armazenando dados do arquivo
            data = file.read(BUFFER_SIZE)

            # Enviando nome do arquivo ao servidor
            print("Enviando nome do arquivo....")
            client_socket.send(FILENAME.encode())

            time.sleep(3)

            while data:
                # Enviando arquivo ao servidor
                print("Enviando arquivo....")
                client_socket.send(data)
                data = file.read(BUFFER_SIZE)

        print("Arquivo enviado...")

    client_socket.close()

if __name__ == '__main__':
    choice = client_menu()

    while choice==1:
        sending_file()

        choice = client_menu()