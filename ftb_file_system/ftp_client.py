from socket import *
import os,sys
import signal
import struct
HOST = '0.0.0.0'
POST = 8888
ADDR = (HOST,POST)

FTP = '/home/tarena/笔记/第二阶段/project/ftp/'


#创建一个类实现文件处理功能
class FTPclient:
    def __init__(self,s):
        self.s = s
        self.count = 0
    def download(self):
        self.count += 1
        self.s.send(b'D')
        data = self.s.recv(128).decode()
        if data == 'OK':
            filename = input('filename>>')
            self.s.send(filename.encode())
            data = self.s.recv(1024)
            filename = "%s%d.txt"%(filename,self.count)
            with open(r'%s'%filename,'wb') as f:
                f.write(data)
                f.flush()
        else:
            print(data)
    def upload(self,):
        self.s.send(b'U')
        data = self.s.recv(128).decode()
        if data == 'OK':
            filename = input('filename>>')
            with open(r'%s%s' % (FTP, filename), 'rb') as f:
                while True:
                    text = f.read(100)
                    self.s.send(text)
                    if not text:
                        self.s.send(b'##')
                        break
    def view(self):
        self.s.send(b'V')
        data = self.s.recv(128).decode()
        if data == 'OK':
            d = self.s.recv(4096).decode()
            #一次接收文件字符串
            print(d)
        else:
            print(data)
    def quit(self):
        self.s.send(b'Q')
        self.s.close()
        sys.exit('客户端退出')

def print_info():
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
    try:
        s.connect(ADDR)
    except  Exception as e:
        print(e)
        return


    ftp = FTPclient(s)
    while True:
        print('==================================')
        print_info()
        print('==================================')
        msg = input('>> ')
        if msg.strip() == 'V':
            ftp.view()
        elif msg.strip() == 'D':
            ftp.download()
        elif msg.strip() == 'U':
            ftp.upload()
        else:
            ftp.quit()







if __name__ == "__main__":
    main()