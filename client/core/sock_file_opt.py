# -*- coding:utf-8 -*-
import os
from client.core.processbar import progress_bar


def file_send(sk,filepath):
    file_size = os.path.getsize(filepath)
    total = file_size
    filename = os.path.basename(filepath)
    # 进度条生成器
    recv_size = 0
    progress_generator = progress_bar(file_size)
    progress_generator.__next__()

    with open(filepath,'rb')as f:
        while file_size > 1024:
            content = f.read(1024)
            sk.send(content)
            file_size -= 1024
            # 进度条
            recv_size += 1024
            progress_generator.send(recv_size)
        else:
            content = f.read()
            if content:
                sk.send(content)
                recv_size += len(content)
                progress_generator.send(recv_size)
        print('---文件 [%s] 发送完成！总大小 [%s]---' % (filename, total))


def file_recv(sk,filename,file_size):
    total = file_size
    # 进度条生成器
    recv_size = 0
    progress_generator = progress_bar(file_size)
    progress_generator.__next__()
    with open(filename,'wb')as f:
        while file_size >1024:
            content = sk.recv(1024)
            f.write(content)
            # 注意每次不一定收到1024，这里用content的长度来做减法
            file_size -= len(content)
            # 进度条
            recv_size += len(content)
            progress_generator.send(recv_size)

        else:
            content = sk.recv(1024)
            if content:
                f.write(content)
                recv_size += len(content)
                progress_generator.send(recv_size)
        print('---文件 [%s] 接收完成！总大小 [%s]---' % (filename, total))