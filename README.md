## 宏伟兄网盘系统
### 运行程序
1、首先切换到程序的根目录（你可以看到server、client目录）

2、启动server端的命令：
```python
python3 -m server.bin.start
```

3、启动server端后，你需要添加用户（选1）—— 默认的client用户名是（whw 123或www 123）

4、注意，启动server端后，选择`2`后才能与客户端建立连接

5、客户端client启动的命令：
```python
python3 -m client.bin.start
```
### 其他说明
1、本程序是自己初学Python时做的一个练习项目，`目录结构的设计`与`降低程序的耦合性`等技巧希望能为Python程序设计的初学者提供一些参考；当然程序内也包含了很多知识点，比如反射、解决TCP传输的粘包现象、递归删除文件夹、subprocess模块获取命令结果、socket客户端的校验等等。

2、不同系统下查看文件的命令都是dir！在后台判断当前操作系统使用对应的命令：ls或dir

3、只能解析两个参数的命令，像get whw.jpg这样的一个参数的命令做了异常处理，多个参数的话 也只能找到命令后的第一个参数
—— 对dir 跟pwd做了特殊处理

4、客户端需要打印进度条 因此客户端的 sock_file_opt.py 文件多了进度条的功能

5、TCP粘包问题，默认不用协议发送：一定要保证字典转为str再转为bytes的长度小于1024（我设置的不用协议接收的大小默认为1024）

6、可以添加自己的用户名密码测试

7、系统会为每个用户在server端的`home`目录中创建以自己名字命名的文件夹，以后用户的所有操作都在这个文件夹中进行！

8、put上传的文件需要提前放到client目录中的`home`文件夹中！get命令从自己server端的文件夹中获取文件并统一存放在client目录中的`download`文件夹中。

9、上传、下载、删除文件或文件夹时必须写完整的文件或文件夹的名字
