import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '26.153.90.162'
port = 2020
s.connect((host, port))
s.send('hello!'.encode())
data = s.recv(1000000)
print('received', data, len(data), 'bytes')
s.close()