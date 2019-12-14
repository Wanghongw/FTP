# -*- coding:utf-8 -*-
import hmac

from client.conf.settings import SECRET_KEY
from client.core.sock_trance_dic import pro_send,pro_recv


def conn_auth(sk):
    '''
    验证客户端到服务器的链接
    '''
    msg = sk.recv(32)
    # 注意 这里是bytes类型的！
    h = hmac.new((SECRET_KEY).encode('utf-8'), msg)
    digest = h.digest()
    sk.sendall(digest)
    # 从server端接收结果
    # server端没用协议 我们也不用
    dic = pro_recv(sk,False)
    # 认证成功
    if dic['ret']:
        return True
    else:
        return False
