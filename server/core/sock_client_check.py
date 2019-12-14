# -*- coding:utf-8 -*-
import os
import hmac
import socket
from server.conf.settings import SECRET_KEY
from server.core.prints import *

def check_client(conn):
    print_correct('有新链接来了！开始验证新链接的合法性...')
    # 返回一个bytes类型的32字节的随机串
    msg_bytes=os.urandom(32)
    # 发给客户端
    conn.sendall(msg_bytes)
    # hmac.new方法
    h=hmac.new(SECRET_KEY.encode('utf-8'),msg_bytes)
    digest=h.digest()
    respone=conn.recv(len(digest))
    return hmac.compare_digest(respone,digest)








