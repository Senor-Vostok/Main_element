import socket
import select
import os

ACK_TEXT = 'text_received'


class Host:
    def __init__(self, port):
        self.PORT = port
        self.HOST = '0.0.0.0'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.array_clients = list()
        self.update = list()

    def send_to(self, message, client):
        self.encode(message, client)

    def encode(self, message, sock):
        encodedMessage = bytes(message, 'utf-8')
        sock.sendall(encodedMessage)

    def encoding(self, sock):
        encode = sock.recv(10**10)
        return encode.decode('utf-8')


host = Host(8080)
host.sock.listen()
while True:
    if len(host.array_clients) < 1:
        print("wait")
        client, adr = host.sock.accept()
        if client not in host.array_clients:
            host.array_clients.append(client)
            with open(rf'{os.getcwd()}\online\Protocols', mode='rt') as file:
                file = file.read().split('-0-')
                host.send_to(file[1], client)
        if len(host.array_clients) == 1:
            with open(rf'{os.getcwd()}\online\Protocols', mode='w') as file:
                file.write('')
                print('protocol cleaned')
        print("CLIENT:", client)
    else:
        ready_socks, _, _ = select.select(host.array_clients, [], [], 0)
        for sock in ready_socks:
            message = host.encoding(sock)
            if len(message.split('-0-')) > 1:
                message = ''.join(message.split(' '))
                with open(rf'{os.getcwd()}\online\Cache', mode='w') as file:
                    print('catch', message)
                    file.write(message)
                for c in host.array_clients:
                    host.send_to(message, c)
        with open(rf'{os.getcwd()}\online\Protocols', mode='rt') as file:
            file = file.read()
            if len(file.split('-0-')) > 1:
                file = ''.join(file.split(' '))
                print('send all', str(file))
                for client in host.array_clients:
                    host.send_to(file, client)
        with open(rf'{os.getcwd()}\online\Protocols', mode='w') as file:
                file.write('')
