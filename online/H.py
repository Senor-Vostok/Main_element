import socket
import os


class Host:
    def __init__(self, port):
        self.PORT = port
        self.HOST = '0.0.0.0'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.array_clients = list()

    def send_to(self, tipe, message, client):
        if tipe == 'm':
            message = ['<start> read_array'] + message + ['<end> read_array']
        for i in range(len(message)):
            self.encode(message[i], client)

    def encode(self, message, sock):
        encodedMessage = bytes(message, 'utf-8')
        sock.sendall(encodedMessage)
        encodedAckText = sock.recv(10000)
        encodedAckText.decode('utf-8')


host = Host(2020)
while True:
    try:
        if len(host.array_clients) < 4:
            host.sock.listen()
            client, adr = host.sock.accept()
            if client not in host.array_clients:
                host.array_clients.append(client)
                with open(rf'{os.getcwd()}\online\Protocols', mode='rt') as file:
                    file = file.read().split('-0-')
                    host.send_to(file[0], file[1].split('\n'), client)
            if len(host.array_clients) == 1:
                print("HOST:", adr)
            if len(host.array_clients) == 4:
                with open(rf'{os.getcwd()}\online\Protocols', mode='w') as file:
                    file.write('\0')
        else:
            with open(rf'{os.getcwd()}\online\Protocols', mode='rt') as file:
                file = file.read().split('-0-')
                if len(file) > 1:
                    for client in host.array_clients:
                        host.send_to(file[0], file[1], client)
    except Exception:
        pass
