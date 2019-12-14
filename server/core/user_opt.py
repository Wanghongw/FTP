# -*- coding:utf-8 -*-
import os
from server.core.prints import *
from server.core.hashlib_opt import make_md5
from server.conf.settings import USER_INFO_PATH,HOME_PATH
from server.core.logger import my_log

def add_user():
    """
    添加用户
    :return:
    """
    while 1:
        username = input('添加的用户名：').strip()
        re_user = input('确认添加的用户名：').strip()
        password = input('密   码：').strip()
        re_password = input('确认密码：').strip()
        if username == re_user and password == re_password:
            md5_pwd = make_md5(username,password)
            with open(USER_INFO_PATH,'r+',encoding='utf-8')as f:
                for line in f:
                    usr,pwd = line.strip().split('|')
                    # print(usr)
                    if usr == username:
                        print_error('用户名已经存在！请重新输入！')
                        # for...else 语句 有这个break，不会执行else的内容了！
                        # 逻辑上：如果有存在的用户名，直接break！
                        break
                else:
                    content = username + '|' + md5_pwd + '\n'
                    f.write(content)
                    # 添加完用户后 在home目录创建一个这个用户的专属文件夹-用户名为名字
                    user_path = os.path.join(HOME_PATH,username)
                    os.makedirs(user_path)
                    # 打印信息 添加日志
                    print_correct('用户 %s 添加成功！'%username)
                    my_log().info('添加了用户 %s '%username)
                    return True
        else:
            print_error('输入信息与确认信息不一致！请确认后再输入！')
