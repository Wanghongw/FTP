# -*- coding:utf-8 -*-
import json
import struct

# 与客户端数据的发送与接收
# 用户自由选择是否利用自定义协议传输
# 但是一定要保证两端的一致性

def pro_send(sk,dic,pro=True):
    """
    发送端需要判断下是否根据协议发送
    """
    str_dic = json.dumps(dic)
    bytes_dic = str_dic.encode('utf-8')
    if pro:
        num_dic = struct.pack('i',len(bytes_dic))
        sk.send(num_dic)
    sk.send(bytes_dic)


def pro_recv(sk,pro=True):
    """
    接收端判断下是否根据协议接收
    """
    if pro:
        bytes_num = sk.recv(4)
        # struct得到的是元组，用索引取出数字
        num = struct.unpack('i',bytes_num)[0]
        # 字典信息
        str_dic = sk.recv(num).decode('utf-8')
        dic = json.loads(str_dic)
        return dic
    # 不根据协议直接用1024个字典收字典即可
    else:
        str_dic = sk.recv(1024).decode('utf-8')
        dic = json.loads(str_dic)
        return dic

