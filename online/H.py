import socket


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
            print(f'{int((i / len(message)) * 100) + 1}%')

    def encode(self, message, sock):
        encodedMessage = bytes(message, 'utf-8')
        sock.sendall(encodedMessage)
        encodedAckText = sock.recv(10000)
        encodedAckText.decode('utf-8')


host = Host(5050)
while True:
    try:
        host.sock.listen()
        client, adr = host.sock.accept()
        if adr not in host.array_clients:
            host.array_clients.append(adr)
            print(host.array_clients)
            with open('Protocols', mode='rt') as file:
                file = file.read().split('-0-')
                host.send_to(file[0], file[1].split('\n'), client)
    except Exception:
        pass
