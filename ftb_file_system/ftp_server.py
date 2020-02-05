from socket import *
from threading import Thread
import os,sys
import signal
import struct
import time
HOST = '0.0.0.0'
POST = 8888
ADDR = (HOST,POST)
st = struct.Struct('2si')
FTP = '/home/tarena/笔记/第二阶段/project/ftp/'

#创建一个类实现文件处理功能
class FTPserver(Thread):
    def __init__(self,c):
        self.c = c
        super().__init__()
        pass
    def download(self):
        self.c.send(b'OK')
        data = self.c.recv(1024).decode()
        with open(r'%s%s'%(FTP,data),'rb') as f:
            while True:
                text = f.read(100)
                self.c.send(text)
                if not text:
                    break

    def upload(self):
        self.c.send(b'OK')
        while True:
            data = self.c.recv(1024)
            with open(r'copy1.txt','ab') as f:
                if data == '##':
                    break
                f.write(data)
                f.flush()
    def view(self):
        data = os.listdir(FTP)
        if not data:
            self.c.send('文件库为空'.encode())
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)
        #拼接文件
        datalist = ''
        for i in data:
            #不是隐藏文件，是普通文件
            if i[0] !='.' and  os.path.isfile(FTP+i):
                datalist += i + "\n"
        self.c.send(datalist.encode())
    def quit(self):
        sys.exit('客户端退出')
    #循环接受请求，分情况调用函数
    def run(self):
        while True:
            data = self.c.recv(128).decode()
            if data == 'V':
                self.view()
            elif data == 'D':
                self.download()
            elif data == 'U':
                self.upload()
            else:
                self.quit()






    '''
    查看，下载，上传，退出
    '''
def request(connfd,ftp):
    msg = connfd.recv(4096)
    data = st.unpack(msg)
    if data[0] == 'V':
        dat = st.pack('V',ftp.view())
        connfd.send(dat)
    elif data[0] == 'U':
        msg = ftp.upload(data[1],)

        connfd.send(msg)
    elif data[0] == 'D':
        ftp.download()
    elif data[0] == 'E':
        ftp.quit()
    return False


def main():
    #网络传输模型
    socketfd = socket()
    socketfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    socketfd.bind(ADDR)
    socketfd.listen(5)
    socketfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print('listen the port 8888...')

    while True:
        try:
            c, addr = socketfd.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            sys.exit('退出服务器')
        except Exception as e:
            print(e)
            continue

        #创建多线程
        t = FTPserver(c)
        t.daemon = True
        t.start()


if __name__ == "__main__":
    main()