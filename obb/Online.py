import socket
import random
import select
import threading


class Client:
    def __init__(self, host, port, nickname):
        self.protocol = 'client'
        self.nickname = nickname
        self.host, self.port = host, int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.loaded_map = False
        self.users = []
        self.gen = ''
        self.maxclient = None
        self.private = False
        self.whitelist = list()
        self.cache = ''

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
            self.cache += message
            if self.cache[-5:] == '-end-':
                info = self.cache[:-5]
                self.cache = ''
                if not self.loaded_map:
                    mess = info.split('-0-')
                    self.loaded_map = True
                    self.gen = mess[0]
                    with open('data/user/information', mode='rt') as uid:
                        uid = uid.read()
                    self.send(f'join-0-{self.nickname}|{uid}-end-')
                    self.maxclient = int(mess[1][0])
                    self.private = bool(int(mess[2][0]) - 1)
                    self.whitelist = mess[3].split('|')
                    if uid not in self.whitelist and self.private:
                        self.sock.close()
                        return 'close'
                    return mess[1][2:]
                else:
                    return info
        return None

    def send(self, message):
        self.sock.sendall(bytes(message, 'utf-8'))

    def __encoding(self, code):
        encode = code.recv(8192)
        message = encode.decode('utf-8')
        code.sendall(bytes(' ', 'utf-8'))
        return ''.join(message.split())


class Host:
    def __init__(self, host, port, gen, maxclient=3, private=False):
        self.protocol = 'host'
        self.host, self.port = host, int(port)
        self.gen = gen
        self.maxclient = maxclient
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.thread = None
        self.in_other_thread = False
        self.private = private
        self.array_clients = list()
        self.users = list()
        self.whitelist = list()

    def send_map(self):
        client, adr = self.sock.accept()
        if client not in self.array_clients:
            self.array_clients.append(client)
            self.send(self.gen + '-0-' + '|'.join([str(self.maxclient)] + self.users) + f'-0-{int(self.private) + 1}-0-{"|".join(self.whitelist)}-end-', client)
            self.in_other_thread = False

    def send(self, message, client=None):
        if not client:
            for client in self.array_clients:
                client.sendall(bytes(message, 'utf-8'))
        else:
            client.sendall(bytes(message, 'utf-8'))

    def hosting(self):
        if len(self.array_clients) < self.maxclient and not self.in_other_thread:
            self.in_other_thread = True
            self.thread = threading.Thread(target=self.send_map)
            self.thread.start()
        ready_socks, _, _ = select.select(self.array_clients, [], [], 0)
        for info in ready_socks:
            message = self.__encoding(info)
            if len(message.split('-0-')) > 1:
                self.send(''.join(message.split()))
                return ''.join(message.split())
        return None

    def __encoding(self, code):
        encode = code.recv(8192)
        message = encode.decode('utf-8')
        return message


class Unknown:
    def __init__(self):
        self.sock = None
        self.protocol = 'unknown'
        self.users = ['i']
        self.maxclient = 0
        self.array_clients = list()
        self.private = False
        self.whitelist = list()

    def send(self, *args):
        pass

    def check_message(self):
        pass

    def hosting(self):
        pass
