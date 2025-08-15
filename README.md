# LittleQQ，一个实现了简单通讯功能的程序
LittleQQ, a simple communication program.



## 使用步骤
首先，确保服务端处于开启状态：运行service.py;\
然后，运行客户端：运行client.py或双击运行LittleQQ.exe;

## 已经实现的功能
注册\
登录\
添加好友\
发送信息\
本地存储信息\
云端存储信息\
用户登录时自动同步下线时所接收的信息\
......\
如果您期待更多的功能，请留言或者私信我让我知道\
如果可以，欢迎给我点一个免费的星星，这对我很重要！
## 注意事项
本程序代码使用的是127.0.0.1作为服务端的ip地址（测试用），如果想开启远程网络通讯功能，仅需将服务端和客户端代码中所包含的所有ip地址更改为建立的服务端的ip地址，再重新使用pyinstaller打包客户端程序发送给客户即可。
```
LittleQQ
├── client.py          #客户端代码
├── service.py         #服务端代码
├── appico.ico         #图标
├── LittleQQ.exe       #客户端可执行文件（通过pyinstaller打包）
