# -*- coding:utf-8 -*-
import os


def file_send(conn,filepath):
    file_size = os.path.getsize(filepath)
    with open(filepath,'rb')as f:
        while file_size > 1024:
            content = f.read(1024)
            conn.send(content)
            file_size -= 1024
        else:
            content = f.read()
            if content:
                conn.send(content)


def file_recv(conn,filename,file_size):
    with open(filename,'wb')as f:
        while file_size > 1024:
            content = conn.recv(1024)
            f.write(content)
            # 不一定收到1024！
            file_size -= len(content)
        else:
            content = conn.recv(1024)
            if content:
                f.write(content)