from socket import *
import os
import signal
import struct
HOST = '0.0.0.0'
POST = 8888
ADDR = (HOST,POST)
st = struct.Struct('2si')


#创建一个类实现文件处理功能
class FTPserver:
    def download(self,filename):
        with open(r'%s'%filename,'rb') as f:
            data = f.read()
    def upload(self,filename,data):
        with open(r'%s'%filename,'wb') as f:
            f.write(data)
    def view(self):
        data = os.listdir('.')
    def quit(self):
        os._exit(0)

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
    socketfd.bind(ADDR)
    socketfd.listen(5)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print('listen the port 8888...')
    while True:
        try:
            connfd, addr = socketfd.accept()
            print('Connect form', addr)
        except KeyboardInterrupt:
            os._exit(0)
        except Exception as e:
            print(e)
            continue
        pid = os.fork()
        ftp = FTPserver()
        if pid == 0:
            ftp = FTPserver()
            request(connfd,ftp)
        else:
            pass



if __name__ == "__main__":
    main()