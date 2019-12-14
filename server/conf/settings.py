# -*- coding:utf-8 -*-
import os

# IP 端口 信息
HOST = '127.0.0.1'
PORT = 9010

# 检测客户端合法性的秘钥
SECRET_KEY = 'Wang_H_W_HERO'
# 设置最大链接数量
MAX_LISTEN = 100

# server基本路径信息
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR,'db')
# 应户名密码文件
USER_INFO_PATH = os.path.join(DB_PATH,'userinfo')
# 日志文件路径
LOG_PATH = os.path.join(BASE_DIR,'log','log.log')
# 用户文件的跟目录 home
HOME_PATH = os.path.join(BASE_DIR,'home')


if __name__ == '__main__':
    print(HOME_PATH)