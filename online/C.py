import socket
import select
import os

HOST = '26.39.51.10'
PORT = 5050

ACK_TEXT = 'text_received'


def main():
    global HOST, PORT
    gen = list()
    start = False
    end = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectionSuccessful = False
    print('connecting...')
    while not connectionSuccessful:
        try:
            with open(rf'{os.getcwd()}\Connect', mode='rt') as file:
                file = (file.read()).split(':')
                HOST, PORT = file[0], file[1]
        except Exception:
            print("ERROR")
        try:
            sock.connect((HOST, PORT))
            connectionSuccessful = True
            print('connecting successful')
        except:
            pass
    socks = [sock]
    while True:
        readySocks, _, _ = select.select(socks, [], [], 5)
        for sock in readySocks:
            message = encoding(sock)
            if not start:
                start = bool("<start> read_array" == message)
            elif start:
                end = bool("<end> read_array" == message)
            if start and not end:
                gen.append([i.split('|') for i in (message.split('\t'))])
            if end:
                with open(rf'{os.getcwd()}\online\Data', mode='w') as file:
                    gen = '\n'.join('\t'.join('|'.join(i) for i in j) for j in gen)
                    file.write(gen)


def do_some():
    pass


def encoding(sock):
    encode = sock.recv(100000)
    if not encode:
        return None
    message = encode.decode('utf-8')
    encode_array = bytes(ACK_TEXT, 'utf-8')
    sock.sendall(encode_array)
    return message


if __name__ == '__main__':
    main()
