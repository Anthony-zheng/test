'''
1.创建监听套接字
２．等待接收客户端请求
３．客户端链接创建新的进程处理客户端请求
４．原进程继续等待其他客户端连接
５．如果客户端退出，则销毁对应的进程
'''
from socket import *
import os
import signal
import struct
HOST = '0.0.0.0'
POST = 8888
ADDR = (HOST,POST)
st = struct.Struct('2si')

#创建套接字
sockefd = socket()
sockefd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockefd.bind(ADDR)
sockefd.listen(5)

#处理僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
print('listen the port 8888...')

def handle(c):
    while True:
        data = c.recv(4096)
        if not data:
            break
        d = st.pack(b'ok',os.getpid())
        c.send(d)
    c.close

while True:
    try:
        connfd,addr = sockefd.accept()
        print('Connect form',addr)
    except KeyboardInterrupt:
        os._exit(0)
    except Exception as e:
        print(e)
        continue

    pid = os.fork()
    if pid == 0:
        # sockefd.close()
        handle(connfd)
        os._exit(0)
    else:
        pass
        # connfd.close()





