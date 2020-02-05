import socket
import struct
st = struct.Struct('2si')
sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_addr = ('127.0.0.1',8888)
sockfd.connect(server_addr)
while True:
    data = input('Msg>>')
    if not data:
        break
    sockfd.send(data.encode())
    data = sockfd.recv(4096)
    data = st.unpack(data)
    print('server',data)
sockfd.close()