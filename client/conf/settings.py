# -*- coding:utf-8 -*-
import os

# IP 端口 信息
HOST = '127.0.0.1'
PORT = 9010

# 检测客户端合法性的秘钥
SECRET_KEY = 'Wang_H_W_HERO'


# server基本路径信息
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# home文件夹的路径
HOME_PATH = os.path.join(BASE_DIR,'home')
DOWNLOAD_PATH = os.path.join(BASE_DIR,'download')



if __name__ == '__main__':
    print(BASE_DIR)
    print(HOME_PATH)
    print(DOWNLOAD_PATH)