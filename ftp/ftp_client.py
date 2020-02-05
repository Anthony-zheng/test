from socket import *
import os
import signal
import struct
HOST = '0.0.0.0'
POST = 8888
ADDR = (HOST,POST)
st = struct.Struct('2si')


#创建一个类实现文件处理功能
class FTPclient:
    def __init__(self,s):
        self.data = s.recv(4096)
    def download(self):
        with open(r'%s'%self.data[1],'wb') as f:
            f.write(self.data)
    def upload(self,):
        with open(r'%s'%self.data[1],'rb') as f:
            text = f.read()
            s.send(text)
    def view(self):
        print(self.data.decode())
    def quit(self):
        if not self.data:
            os._exit(0)
def print_info:
    '''
    ＊下载　Ｄ
    ＊上传　Ｕ
    ＊查看　Ｖ
    ＊退出　Ｅ
    :return:
    '''
    print('－请选择功能－')
    print("文件下载　　　Ｄ")
    print('文件上传　　　Ｕ')
    print('查看文件目录　Ｖ')
    print('退出      　 Ｅ')



def main():
    s = socket()
    s.connect(ADDR)


    while True:
        print_info()
        msg = input('>> \r\n')
        s.send(msg.encode())
        data= s.recv(4096)
        if data.decode() == 'OK':
            print('准备就绪')


    pid = os.fork()

    if pid < 0 :
        sys.exit('Error')
    elif pid == 0:
        send_msg(s)#子进程发消息
    else:
        recv_msg(s)
        #父进程收消息

def send_msg(s):
    while True:
        try:
            section = input('selection >>')
            filename = input('filename>>')
            msg = st.pack(section.encode(),filename.encode())
        except KeyboardInterrupt:
            msg = 'E'
        s.send(msg)

def recv_msg(s):
    ftp = FTPclient(s)
    while True:
        msg = s.recv(4096)
        data = st.unpack(msg).decode()
        if data[0].decode() == 'V':
            ftp.view()
        elif data[0].decode()== 'U':
            ftp.upload()
        elif data[0].decode() == 'D':
            ftp.download()
        else:
            ftp.quit()




if __name__ == "__main__"
    main()