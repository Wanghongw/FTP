# -*- coding:utf-8 -*-
import socket
import socketserver
from server.core.prints import *
from server.core.logger import my_log
from server.core.sock_login import login
from server.core.ftp_server import Server
from server.conf.settings import HOST,PORT,MAX_LISTEN
from server.core.sock_client_check import check_client
from server.core.sock_trance_dic import pro_send



def start_server():
    # 创建socket对象
    sk = socket.socket()
    # 设置端口重复利用
    sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sk.bind((HOST,PORT))
    sk.listen(MAX_LISTEN)
    print_error('Listening......')
    # 链接循环 模拟服务器不down机 因此不进行sk.close()
    while 1:
        # 如果一开始client没登录就强制退出会抛异常
        try:
            conn,addr = sk.accept()
            # 先检测客户端的合法性
            ret = check_client(conn)
            # 表示链接合法
            if ret:
                # 给客户端一个成功的信号字典
                dic = {'opt':'auth','ret':True}
                # 只发送字典，后面没有其他数据 不用协议
                pro_send(conn,dic,False)
                print('客户端 %s 认证成功！'%((addr,)))
                # 认证成功就可以登录了
                ret = login(conn)
                # 登陆成功可以进行接下来的操作
                if ret:
                    print_correct('客户端用户 %s 成功登陆！'%(ret))
                    my_log().info('客户端用户 %s 成功登陆' % (ret))

                    # 成功登陆后就可以实例化一个ftp对象进行接下来的操作了
                    server = Server(ret,conn)
                    server.handle()

                else:
                    # 注意元组作为单个参数格式化的坑
                    print_correct('客户端 %s 登陆失败'%((addr,)))
                    my_log().info('客户端 %s 登陆失败'%((addr,)))
                    conn.close()
            # 链接不合法
            else:
                # 给客户端一个失败的信号字典
                dic = {'opt': 'auth', 'ret': False}
                # 只发送字典，后面没有其他数据 不用协议
                pro_send(conn, dic, False)
                print_error('客户端 %s 认证失败'%((addr,)))
                my_log().error('客户端 %s 认证失败'%((addr,)))
                conn.close()
        except ConnectionResetError:
            continue