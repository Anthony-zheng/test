from multiprocessing import Process
import os
import signal
import struct
from socket import *
HOST = '0.0.0.0'
POST = 8888
ADDR = (HOST,POST)
st = struct.Struct('2si')

socketfd = socket()
socketfd.bind(ADDR)
socketfd.listen(5)
socketfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
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
        c,addr = socketfd.accept()
        print('Connect from',addr)
    except KeyboardInterrupt:
        os._exit(0)
    except Exception as e:
        print(e)
        continue
    p = Process(target=handle,args=(c,))
    c.close()
    p.daemon = True
    p.start()
    socketfd.close()
