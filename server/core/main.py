# -*- coding:utf-8 -*-
import sys

from server.core.prints import *
from server.core.user_opt import add_user
from server.core.sock_abc import start_server

def main():
    operate_dic = {
        '1':['添加用户','add_user'],
        '2':['启动FTP服务器','start_server'],
        '3':['退出','exit'],
    }
    while 1:
        print_correct('【宏伟兄网盘】系统服务端'.center(25,'*'))
        for i in operate_dic:
            print(i,':',operate_dic[i][0])
        choice = input('请输入你要进行的操作编号：').strip()
        if choice not in ['1','2','3']:
            print_error('请输入正确的操作序号！')
        elif choice == '3':
            exit_msg('退出系统！')
        else:
            # 反射
            if hasattr(sys.modules[__name__],operate_dic[choice][1]):
                method = getattr(sys.modules[__name__],operate_dic[choice][1])
                method()

if __name__ == '__main__':
    main()