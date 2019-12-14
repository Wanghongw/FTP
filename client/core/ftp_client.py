# -*- coding:utf-8 -*-
import os
from client.core.prints import *
from client.conf.settings import HOME_PATH,DOWNLOAD_PATH
from client.core.hashlib_opt import get_file_md5
from client.core.sock_file_opt import file_send,file_recv
from client.core.sock_trance_dic import pro_recv,pro_send



class Client(object):
    def __init__(self,username,sk):
        self.username = username
        self.sk = sk
        # self.current_dir = None

    def show_operate(self):
        operate_dic = {
            '1':'查看目录 dir',
            '2':'切换目录 cd',
            '3':'查看当前目录 pwd',
            '4':'新建目录 mkdir',
            '5':'上传文件 put',
            '6':'下载文件 get',
            '7':'删除目录/文件 del',
            '8':'退出系统 exit()',
        }
        print_correct('你可以进行的操作有：')
        for i in operate_dic:
            print(operate_dic[i])

    def run(self):
        try:
            while 1:
                user_input = input('【%s】>>>:'%self.username).strip()
                if not user_input:
                    continue
                # 将命令按照 空格 切片  get xx  put xx ...
                cmd_lis = user_input.split()
                if user_input == 'exit()':
                    exit('用户 %s 退出系统'%self.username)
                # 反射
                elif hasattr(self,'my_%s'%cmd_lis[0]):
                    try:

                        # dir这个命令比较特殊——后面不带参数表示当前目录
                        if user_input == 'dir':
                            # 用户只输入了dir 没跟参数
                            if len(cmd_lis) == 1:
                                dic = {'opt': 'dir', 'arg': ''}
                            else:
                                dic = {'opt': cmd_lis[0], 'arg': cmd_lis[1]}
                            pro_send(self.sk, dic, False)
                            self.my_dir(dic['arg'])
                        # pwd 这个命令比较特殊——后面不带参数
                        elif user_input == 'pwd':
                            # 直接执行pwd函数
                            self.my_pwd()

                        else:
                            method = getattr(self,'my_%s'%cmd_lis[0])
                            # 将命令及参数发给server端 不用协议
                            dic = {'opt':cmd_lis[0],'arg':cmd_lis[1]}
                            pro_send(self.sk,dic,False)
                            # 执行这个方法 注意参数是第二个输入的内容
                            method(cmd_lis[1])
                    except IndexError:
                        print_error('输入有误！')
                else:
                    print_error('系统没有这个命令')
        except Exception as e:
            print_error(e)

    def my_dir(self,arg):
        # print('dir...',arg)
        # 接收server端的结果 用协议!结果可能会很大，会产生粘包
        dic = pro_recv(self.sk)
        total_size = dic['total_size']
        # 接收规则：
        recv_size = 0
        recv_data = self.sk.recv(total_size)
        # while recv_size < total_size:
        #     # 每次接收1024
        #     ret = self.sk.recv(1024)
        #     recv_data += ret
        #     # 注意recv_size 每次加接收数据的长度——每一次不一定收1024
        #     recv_size += len(ret)
        # else:
        #     ret = self.sk.recv(1024)
        #     if ret:
        #         recv_data += ret
        # # 注意 win系统 解码成 gbk
        cmd_ret = recv_data.decode('gbk')
        print(cmd_ret)


    def my_cd(self,arg):
        # print('cd...',arg)
        # 不用协议接收返回的字典 dic = {'ret':False,'ret_lis':[]}
        dic = pro_recv(self.sk,False)
        if not dic['ret']:
            print_error(dic['ret_lis'][0])


    def my_pwd(self):
        # print('pwd...')
        dic = {'opt': 'pwd', 'arg': ''}
        # 直接发给server, server做反射时不用协议接收 这里也不用协议
        pro_send(self.sk,dic,False)
        # 接收结果  {'ret':self.current_dir}
        dic = pro_recv(self.sk,False)
        print_correct('当前路径为：%s'%dic['ret'])


    def my_mkdir(self,arg):
        # print('mkdir...',arg)
        # 接收结果字典 dic = {'ret':False,'msg':None}
        dic = pro_recv(self.sk,False)
        if not dic['ret']:
            print_error(dic['msg'])
        else:
            print_correct('创建目录成功！')


    def my_put(self,arg):
        print('put...',arg)
        # 默认传home文件夹中的文件 —— “模拟本地”
        filepath = os.path.join(HOME_PATH,arg)
        if os.path.isfile(filepath) and os.path.exists(filepath):
            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath)
            file_md5 = get_file_md5(filepath)
            dic = {'file_exists':True,'filename':filename,'file_size':file_size,'file_md5':file_md5}
            # 将字典传给server——用协议 因为接着后面会传文件！
            pro_send(self.sk,dic)
            # 开始传文件 —— file_size参数是为了打印进度条的
            file_send(self.sk,filepath)
            # 不用协议 收结果  dic = {'ret':False}
            ret = pro_recv(self.sk,False)
            if not ret['ret']:
                print_error('文件传输的过程有损坏！')
            else:
                print_correct('文件传输完成，经校验无误！')
        else:
            print_error('你的home文件夹中没有这个文件！')
            # 注意 由于arg参数已经传给server了，因此把错误的信息还得发给server，让那边做判断
            dic = {'file_exists': False}
            # 将字典传给server——用协议
            pro_send(self.sk, dic)


    def my_get(self,arg):
        print('get...',arg)
        # 接收结果的字典
        dic = pro_recv(self.sk) # {'exists':False,'filename':None,'file_size':None,'msg':'','file_md5':None}
        if not dic['exists']:
            print_error(dic['msg'])
        else:
            filename = dic['filename']
            file_size = dic['file_size']
            file_md5 = dic['file_md5']
            # 开始接收文件
            # 默认接收到download文件夹中
            download_path = os.path.join(DOWNLOAD_PATH,filename)
            file_recv(self.sk,download_path,file_size)
            recv_file_md5 = get_file_md5(download_path)
            # 返回给server的结果字典 {'ret':True} 不用协议发
            if recv_file_md5 == file_md5:
                dic = {'ret':True}
                pro_send(self.sk,dic,False)
                print_correct('文件传输完成，经校验后无误！')


    def my_del(self,arg):
        print('del...',arg)
        # 接收server端返回的字典 不用协议
        dic = pro_recv(self.sk,False) #dic = {'ret':False,'msg':None}
        if not dic['ret']:
            print_error(dic['msg'])
        else:
            print_correct('成功删除 %s'%arg)
