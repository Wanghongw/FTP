# -*- coding:utf-8 -*-
import os
import hashlib


def make_md5(username,password):
    md5 = hashlib.md5(username.encode('utf-8'))
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

def get_file_md5(filepath):
    filesize = os.path.getsize(filepath)
    md5 = hashlib.md5()
    if os.path.isfile(filepath):
        with open(filepath,'rb')as f:
            while filesize > 2048:
                content = f.read(2048)
                md5.update(content)
                filesize -= 2048
            else:
                content = f.read()
                if content:
                    md5.update(content)
        return md5.hexdigest()
    else:
        return None



if __name__ == '__main__':
    print(make_md5('whw','cf')) #beff47926b075d606900a6c6db13645a
    print(get_file_md5('D:\\0.0电影\暴雪将至.mp4'))#6a37f182c3501c4d328760818439efa5