import socket
import select
import threading


class Client:
    def __init__(self, host, port):
        self.protocol = 'client'
        self.host, self.port = host, int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.loaded_map = False
        self.gen = None

    def connecting(self):
        try:
            self.sock.connect((self.host, self.port))
            return True
        except Exception:
            return False

    def check_message(self):
        ready_socks, _, _ = select.select([self.sock], [], [], 0)
        for info in ready_socks:
            message = self.__encoding(info)
            if not self.loaded_map:
                self.gen = message
                self.loaded_map = True
                print('loaded')
            else:
                print('catch', message)
                return ''.join(message.split(' '))
        return None

    def send(self, message):
        self.sock.sendall(bytes(message, 'utf-8'))

    def __encoding(self, code):
        encode = code.recv(10 ** 7)
        message = encode.decode('utf-8')
        code.sendall(bytes('get it', 'utf-8'))
        return message


class Host:
    def __init__(self, host, port, gen, maxclient=3):
        self.protocol = 'host'
        self.host, self.port = host, int(port)
        self.gen = gen
        self.maxclient = maxclient
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.thread = threading.Thread(target=self.send_map)
        self.thread.start()
        self.in_other_thread = True
        self.array_clients = list()

    def send_map(self):
        client, adr = self.sock.accept()
        if client not in self.array_clients:
            self.array_clients.append(client)
            self.send(self.gen, client)

    def send(self, message, client=None):
        if not client:
            for client in self.array_clients:
                client.sendall(bytes(message, 'utf-8'))
        else:
            client.sendall(bytes(message, 'utf-8'))

    def hosting(self):
        if len(self.array_clients) == self.maxclient and self.in_other_thread:
            self.thread.join()
            self.in_other_thread = False
        elif len(self.array_clients) == self.maxclient and not self.in_other_thread:
            ready_socks, _, _ = select.select(self.array_clients, [], [], 0)
            for info in ready_socks:
                message = self.__encoding(info)
                if len(message.split('-0-')) > 1:
                    self.send(''.join(message.split(' ')))
                    return ''.join(message.split(' '))
        return None

    def __encoding(self, code):
        encode = code.recv(10 ** 7)
        message = encode.decode('utf-8')
        return message


class Unknown:
    def __init__(self):
        self.protocol = 'unknown'

    def send(self, *args):
        pass

    def check_message(self):
        pass

    def hosting(self):
        pass
