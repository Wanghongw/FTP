# -*- coding:utf-8 -*-
import os
import sys
import socketserver
import subprocess
from server.core.prints import *
from server.core.logger import my_log
from server.core.del_dir import del_dir
from server.core.hashlib_opt import get_file_md5
from server.core.sock_file_opt import file_send,file_recv
from server.conf.settings import HOME_PATH
from server.core.sock_trance_dic import pro_send,pro_recv


class Server(object):
    def __init__(self,username,conn):
        self.username = username
        self.conn = conn
        # 用户当前目录的信息 ———— 非常关键的参数！
        self.current_dir = None


    def handle(self):

        # 先记录用户当前在哪个目录，如果登录了就默认在自己名字的根目录，后续操作全靠它！
        self.current_dir = os.path.join(HOME_PATH,self.username)

        # 循环接收
        while 1:
            # 远程主机强制关闭会抛异常
            try:
                # 接收客户端的命令字典 不用协议
                dic = pro_recv(self.conn, False)  # {'opt':cmd_lis[0],'arg':cmd_lis[1]}
                opt = dic['opt']
                arg = dic['arg']
                # 反射 客户端进行命令验证，因此发来的一定是有效的命令
                if hasattr(self, 'my_%s' % opt):
                    try:
                        method = getattr(self, 'my_%s' % opt)
                        method(arg)
                    except Exception as e:
                        print_error(e)
            except Exception as e:
                print_error(e)
                self.conn.close()
                break


    def my_dir(self,arg):
        # 每个用户只能dir查看自己目录下列表 —— 自己的根目录就是自己用户名的文件夹
        self_path = os.path.join(self.current_dir,arg)
        # 获取当前操作系统类型：ls适用于mac与linux，dir适用于windows
        platform = sys.platform
        # windows系统
        if platform.startswith("win") or platform.startswith("cygwin"):
            # subprocess模块得到命令
            cmd_obj = subprocess.Popen('dir %s'%self_path,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        # mac或linux
        else:
            cmd_obj = subprocess.Popen('ls %s' % self_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        stderr = cmd_obj.stderr.read()
        # 这是bytes类型的！
        cmd_ret = stdout + stderr
        if not cmd_ret:
            cmd_ret = '你的目录没得文件，请创建目录'
        #  # 将命令结果返回给客户端-结果可能会很大，产生粘包-因此用协议发送
        size = len(stdout) + len(stderr)
        # 先告诉客户端大小信息
        dic = {'total_size':size}
        pro_send(self.conn,dic)
        #再发送真实数据
        self.conn.send(stdout)
        self.conn.send(stderr)


    def my_cd(self,arg):
        print('cd   ',arg)
        # 给客户端返回的信息字典 ret为True表示有效的命令;为False的话无效，并且ret_lis返回信息
        dic = {'ret':False,'ret_lis':[]}
        # 当前用户的“跟目录” 为self.current_dir
        input_path = os.path.join(self.current_dir,arg)
        if arg == '.':
            dic = {'ret': True, 'ret_lis': []}
        elif arg == '..':
            if os.path.basename(self.current_dir) == self.username:
                dic['ret_lis'] = ['不能往前了！']
            else:
                # 当前路径往前退一个 dirname！
                self.current_dir = os.path.dirname(self.current_dir)
                dic = {'ret': True, 'ret_lis': []}
        elif os.path.isdir(input_path):
            dic = {'ret': True, 'ret_lis': []}
            self.current_dir = input_path
        elif os.path.isfile(input_path):
            dic['ret_lis'] = ['这是个文件，不是目录！']
        else:
            dic['ret_lis'] = ['没有这个目录！']
        # 将结果字典返回给client 不用协议
        pro_send(self.conn,dic,False)


    def my_pwd(self,arg):
        print('pwd   ')
        # 将当前的路径返回就OK了 不用协议
        dic = {'ret':self.current_dir}
        pro_send(self.conn,dic,False)


    def my_mkdir(self,arg):
        print('mkdir   ',arg)
        # 返回的信息字典
        dic = {'ret':False,'msg':None}

        sub_path = os.path.join(self.current_dir,arg)
        if os.path.isdir(sub_path):
            dic['msg'] = '改目录已经存在了！'
        # 用异常处理无效的目录名
        try:
            os.makedirs(sub_path)
            dic['ret'] = True
        except Exception as e:
            dic['msg'] = '无效的目录名！'

        # 最后将字典返回给client 不用协议
        pro_send(self.conn,dic,False)


    def my_put(self,arg):
        print('put   ',arg)
        # 根据协议 先收字典
        dic = pro_recv(self.conn) # {'file_exists':True,'filename':filename,'file_size':file_size,'file_md5':file_md5}
        # 先判断下client端是否正常
        if dic['file_exists']:
            filename = dic['filename']
            file_size = dic['file_size']
            file_md5 = dic['file_md5']
            # 需要将文件put到“当前的目录”！不判断文件是否存在，wb写直接覆盖掉
            file_put_path = os.path.join(self.current_dir,filename)
            # 接收文件
            file_recv(self.conn,file_put_path,file_size)
            # 返回的信息
            dic = {'ret':False}
            new_file_md5 = get_file_md5(file_put_path)
            if new_file_md5 == file_md5:
                dic['ret'] = True
                # 写日志
                my_log().warning('用户 %s 成功上传了文件 %s'%(self.username,filename))
            # 不用协议发结果
            pro_send(self.conn,dic,False)
        # 否则 不做任何操作
        else:
            pass


    def my_get(self,arg):
        print('get   ',arg)
        # 返回的字典
        dic = {'exists':False,'filename':None,'file_size':None,'msg':'','file_md5':None}
        filepath = os.path.join(self.current_dir,arg)
        if os.path.isfile(filepath):
            dic['exists'] = True
            dic['filename'] = arg
            dic['file_size'] = os.path.getsize(filepath)
            # 获取文件的md5值
            file_md5 = get_file_md5(filepath)
            dic['file_md5'] = file_md5
            # 协议 发送字典
            pro_send(self.conn,dic)
            # 然后发送 文件数据
            file_send(self.conn,filepath)
            # 从client端接收一个成功的字典用来写日志 {'ret':True} 不用协议
            ret = pro_recv(self.conn,False)
            if ret['ret']:
                my_log().warning('用户 %s 从服务器下载了文件 %s'%(self.username,arg))

        elif os.path.isdir(filepath):
            dic['msg'] = '你不能下载一个文件夹！'
            pro_send(self.conn,dic)
        else:
            # 用协议发送字典——因为client端一定会用协议接收的
            dic['msg'] = '没有这个文件！'
            pro_send(self.conn,dic)


    def my_del(self,arg):
        print('del   ',arg)
        filepath = os.path.join(self.current_dir,arg)
        # 返回的信息字典
        dic = {'ret':False,'msg':None}

        if os.path.isfile(filepath):
            os.remove(filepath)
            dic['ret'] = True
            # 日志
            my_log().warning('用户 %s 删除了文件 %s'%(self.username,arg))
        # 如果是目录的话 得判断下 不能删除当前用户的“根目录”
        elif os.path.isdir(filepath):
            if os.path.basename(filepath) == self.username:
                dic['msg'] = '大兄弟！你不能删除你的根目录！'
            else:
                dic['ret'] = True
                del_dir(filepath)
                # 然后记得把 self.current_dir 的值往前调整1位！
                # self.current_dir = os.path.dirname(self.current_dir)
                # 日志
                my_log().warning('用户 %s 删除了文件夹 %s'%(self.username,arg))
        else:
            dic['msg'] = '没有这个文件或目录！'
        # 统一返回 不用协议
        pro_send(self.conn,dic,False)

