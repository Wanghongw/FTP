# -*- coding:utf-8 -*-


from client.core.sock_trance_dic import pro_recv,pro_send

def login(sk):
    username = input('请输入用户名：').strip()
    password = input('请输入密码：').strip()
    dic = {'opt':'login','username':username,'password':password}
    # 用协议传输
    pro_send(sk,dic)
    # 接收结果字典 不用协议
    ret_dic = pro_recv(sk,False)
    if ret_dic['ret']:
        # 返回用户名
        return username
    else:
        return False
