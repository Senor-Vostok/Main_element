import socket
import select
import os

HOST = '26.39.51.10'
PORT = 2020

ACK_TEXT = 'text_received'


def main():
    global HOST, PORT
    loaded = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    connection_successful = False
    print('connecting...')
    while not connection_successful:
        try:
            with open(rf'{os.getcwd()}\online\Connect', mode='rt') as file:
                file = (file.read()).split(':')
                HOST, PORT = file[0], int(file[1])
        except Exception:
            print("ERROR")
        print(HOST, PORT)
        sock.connect((HOST, PORT))
        connection_successful = True
        print('connecting successful')
    while True:
        ready_socks, _, _ = select.select([sock], [], [], 0)
        for sock in ready_socks:
            message = encoding(sock)
            if len(message.split('-0-')) == 1 and not loaded:
                loaded = True
                with open(rf'{os.getcwd()}\online\Save', mode='w') as file:
                    print('load complete')
                    file.write(message)
            else:
                with open(rf'{os.getcwd()}\online\Cache', mode='w') as file:
                    send_to('thanks', sock)
                    print('catch', message)
                    file.write(message)
                    continue
        with open(rf'{os.getcwd()}\online\Protocols', mode='rt') as file:
            file = ''.join(file.read().split(' '))
            send_to(file, sock)
            send = True
        if send:
            with open(rf'{os.getcwd()}\online\Protocols', mode='w') as file:
                file.write('')
                send = False


def encoding(sock):
    encode = sock.recv(10**10)
    message = encode.decode('utf-8')
    encode_array = bytes(ACK_TEXT, 'utf-8')
    sock.sendall(encode_array)
    return message


def encode(message, sock):
    encodedMessage = bytes(message, 'utf-8')
    sock.sendall(encodedMessage)


def send_to(message, client):
    encode(message, client)


if __name__ == '__main__':
    main()
