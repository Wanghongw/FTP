# -*- coding:utf-8 -*-
import socket

from client.core.prints import *
from client.conf.settings import HOST,PORT
from client.core.sock_server_check import conn_auth
from client.core.sock_login import login
from client.core.ftp_client import Client


def main():
    # 创建socket对象并建立链接
    sk = socket.socket()
    sk.connect((HOST,PORT))

    # 进行客户端认证
    ret = conn_auth(sk)
    if ret:
        print_correct('认证成功！开始登录！')
        # 登陆
        ret = login(sk)
        if ret:
            print_correct('欢迎进入【宏伟兄网盘】系统'.center(25,'*'))
            # 实例化一个client对象
            client = Client(ret,sk)
            # 进行具体操作
            client.show_operate()
            # 客户端开始操作！
            client.run()

        else:
            print_error('登陆失败！用户名或密码错误！')
    else:
        print_error('认证失败，请检查你的秘钥是否正确！')
        sk.close()

if __name__ == '__main__':
    main()
