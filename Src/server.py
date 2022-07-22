from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = "localhost"
PORT = 55000
BUFF_SIZE = 1024
ADDRESS = (HOST, PORT)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(ADDRESS)


def accept_connections():
    while True:
        client, client_address = server_socket.accept()
        print("%s:%s está online." % client_address)
        client.send(bytes("Digite o seu nome:", "utf8"))
        addresses[client] = client_address
        Thread(target=connect_client, args=(client,)).start()


def server_broadcast(msg, prefix=""):


    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def connect_client(client):

    name = client.recv(BUFF_SIZE).decode("utf8")

    welcome = "Bem-vindo "
    client.send(bytes(welcome + name + "!", "utf8"))
    client.send(bytes("O chat foi ativado!", "utf8"))
    msg = "%s entrou no chat!" % name
    server_broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFF_SIZE)
        if msg != bytes("{disconnect}", "utf8"):
            server_broadcast(msg, name + "")
        else:
            client.send(bytes("{disconnect}", "utf8"))
            client.close()

            del clients[client]
            server_broadcast(bytes("%s saiu do chat" % name, "utf8"))
            break


if __name__ == "__main__":
    server_socket.listen(5)
    print("Aguardando conexão...")
    accept_thread = Thread(target=accept_connections)
    accept_thread.start()
    accept_thread.join()
server_socket.close()