import socket
import select

HOST = 'localhost'
PORT = 5050

ACK_TEXT = 'text_received'


def main():
    gen = list()
    start = False
    end = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectionSuccessful = False
    while not connectionSuccessful:
        try:
            sock.connect((HOST, PORT))
            connectionSuccessful = True
        except:
            pass
    socks = [sock]
    while True:
        readySocks, _, _ = select.select(socks, [], [], 5)
        for sock in readySocks:
            message = encoding(sock)
            if start and not end:
                gen.append([i.split('|') for i in (message.split('\t'))])
            if not start:
                start = bool("<start> read_array" == message)
            elif start:
                end = bool("<end> read_array" == message)
            if end:
                print(gen)


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