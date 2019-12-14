# -*- coding:utf-8 -*-

from server.core.hashlib_opt import make_md5
from server.conf.settings import USER_INFO_PATH
from server.core.sock_trance_dic import pro_send,pro_recv

def login(sk):
    # 用协议接收
    dic = pro_recv(sk)
    if dic['opt'] == 'login':
        username = dic['username']
        password = dic['password']
        with open(USER_INFO_PATH,'r',encoding='utf-8')as f:
            for line in f:
                usr,pwd = line.strip().split('|')
                if usr == username and pwd == make_md5(username,password):
                    # 给客户端发一个成功的字典信息—— 不用协议
                    # 同时给server端返回结果
                    ret_dic =  {'opt':'login','ret':True }
                    pro_send(sk,ret_dic,False)
                    # 把用户名返回去
                    return username
            else:
                # 给客户端发一个失败的字典信息—— 不用协议
                # 同时给server端返回结果
                ret_dic = {'opt': 'login', 'ret': False}
                pro_send(sk, ret_dic, False)
                return False

    else:
        # 给客户端发一个失败的字典信息—— 不用协议
        # 同时给server端返回结果
        ret_dic = {'opt': 'login', 'ret': False}
        pro_send(sk, ret_dic, False)
        return False