# -*- coding:utf-8 -*-
import os

def del_dir(filepath):
    lis = [filepath]
    lst = []
    while lis:
        path = lis.pop()
        for f in os.listdir(path):
            sub_path = os.path.join(path,f)
            if os.path.isfile(sub_path):
                os.remove(sub_path)
            elif os.path.isdir(sub_path):
                lis.append(sub_path)
                lst.append(sub_path)
    # 把所有文件删完后，再处理里面的空文件夹
    # 注意这里 倒序 取！从里往外删
    for f in lst[::-1]:
        os.rmdir(f)
    # 最后再把最外面的目录删掉 —— 整个目录就没得了
    os.rmdir(filepath)