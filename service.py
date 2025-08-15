import socket
import threading
import time
import csv
import os
#cd /d D:tkinter-learning
#python3 service.py

#初始化生成必要文件（夹）
if not os.path.exists("userlist.csv"):
    with open('userlist.csv','w',encoding='utf-8',newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['用户名','密码'])
if not os.path.exists("user"):
    script_dir=os.path.dirname(os.path.abspath(__file__))
    user_dir=os.path.join(script_dir,"user")
    os.makedirs(user_dir)


def tcplink(sock,addr):
    print('连接到一个客户端___%s:%s___'%addr)
    userlist=open("userlist.csv",'r',encoding='utf-8',newline='')
    uu=""
   
    while True:
        
        data=sock.recv(1024)
        x=data.decode('utf-8').split('|')
        time.sleep(0.2)

        #100为注册申请
        if x[0]=="100":
            username=x[1].strip()
            password=x[2].strip()
            flag=True
            try:
                with open('userlist.csv','r+',encoding='utf-8',newline='') as file:
                    for line in file:
                        li=line.split(',')
                        if username==li[0] or username=="":
                            message100="注册失败，用户名已存在"
                            flag=False
                            break
                if flag:                 
                    with open('userlist.csv','a+',encoding='utf-8',newline='') as file:
                        writer=csv.writer(file)
                        writer.writerow([username,password])
                    p=username+"chat.txt"
                    p2="friendlist.txt"
                    script_dir=os.path.dirname(os.path.abspath(__file__))
                    user_dir=os.path.join(script_dir,"user")
                    file_path0=os.path.join(user_dir,username)
                    os.mkdir(file_path0)
                    file_path=os.path.join(file_path0,p)
                    with open(file_path,"w",encoding='utf-8')as file:
                        pass
                    file_path2=os.path.join(file_path0,p2)
                    with open(file_path2,"w",encoding='utf-8')as file:
                        pass
                    
                    message100="注册成功"
                sock.send(message100.encode('utf-8'))
            except Exception as e:
                sock.send("未知错误".encode('utf-8'))
        
        #000为用户名提交
        if x[0]=="000":
            print("用户名为:"+x[1])
            uu=x[1]
        #001为登录请求
        if x[0]=="001":
            userlist=open("userlist.csv",'r',encoding='utf-8',newline='')
            username=x[1]
            password=x[2]
            flag=False
            for line in userlist:
                line=line.strip()
                user=line.split(',')
                if str(user[0])==str(username) and str(user[1])==str(password):
                    flag=True
                    break
            if flag:
                sock.send("PASS".encode('utf-8'))


                def sender(sock):
                    #云端聊天记录加载
                    while True:
                        time.sleep(1)
                        p=username+"chat.txt"
                        script_dir=os.path.dirname(os.path.abspath(__file__))
                        user_dir=os.path.join(script_dir,"user")
                        file_path0=os.path.join(user_dir,username)
                        file_path=os.path.join(file_path0,p)
                        chatlist=open(file_path,"r+",encoding='utf-8')
                        lines=chatlist.readlines()
                        for line in lines:
                            if line=="":
                                continue
                            myline=line.strip().split('|')                    
                            messxx3="xx3|"+myline[0]+'|'+myline[2]+'|'+myline[3]+'\n'
                            sock.send(messxx3.encode('utf-8'))
                        chatlist.close()
                        chatlist=open(file_path,"w",encoding='utf-8')
                        chatlist.close()
                threading.Thread(target=sender,args=(sock,)).start()
                
                def senfri(sock):
                    #云端好友信息加载
                    print("开始同步")
                    while True:
                        p="friendlist.txt"
                        script_dir=os.path.dirname(os.path.abspath(__file__))
                        user_dir=os.path.join(script_dir,"user")
                        file_path0=os.path.join(user_dir,username)
                        file_path=os.path.join(file_path0,p)
                        frilist=open(file_path,"r+",encoding='utf-8')
                        lines=frilist.readlines()
                        if len(lines)!=0:
                
                            for line in lines:
                      
                                if line=="":
                                    continue
                                myline=line.split('|')                    
                                messxx5="xx5|"+myline[0].strip()+'|'+myline[1].strip()+'\n'
                                sock.send(messxx5.encode('utf-8'))
                                time.sleep(0.5)
                
                            frilist.close()
                            frilist=open(file_path,"w",encoding='utf-8')
                            frilist.close()
                        time.sleep(5)
                threading.Thread(target=senfri,args=(sock,)).start()

                

                
            else :
                sock.send("NOTPASS".encode('utf-8'))
            userlist.close()
        #002开头为发送请求
        if x[0]=="002":
            p=x[2]+"chat.txt"
            script_dir=os.path.dirname(os.path.abspath(__file__))
            user_dir=os.path.join(script_dir,"user")
            file_path0=os.path.join(user_dir,x[2])
            file_path=os.path.join(file_path0,p)
            chatlist=open(file_path,"a+",encoding='utf-8')
            mess002=x[3]+'|'+x[2]+'|'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'|'+x[1]+'\n'
            chatlist.write(mess002)
            sock.send("xx2|发送成功".encode('utf-8'))
            chatlist.close()
        #004开头为添加好友请求
        if x[0]=="004":
            flag=True
            with open('userlist.csv','r+',encoding='utf-8',newline='') as file:
                for line in file:
                    li=line.split(',')
                    if username==li[0]:
                        message004="xx4|添加成功"
                        flag=False
                        break
            if flag:
                message004="xx4|添加失败，该好友不存在"
            
            try:
                p="friendlist.txt"
                script_dir=os.path.dirname(os.path.abspath(__file__))
                
                user_dir=os.path.join(script_dir,"user")
                file_path0=os.path.join(user_dir,x[2])
                file_path=os.path.join(file_path0,p)

                with open(file_path,"a+",encoding='utf-8') as file:
                    #x开头为添加
                    file.write("x|"+x[1]+'\n')

            except Exception as e:
                message004="xx4|Error"
            sock.send(message004.encode('utf-8'))
        #005开头为删除好友
        if x[0]=="005":
            p="friendlist.txt"
            script_dir=os.path.dirname(os.path.abspath(__file__))
            user_dir=os.path.join(script_dir,"user")
            file_path0=os.path.join(user_dir,x[2])
            file_path=os.path.join(file_path0,p)            
            with open(file_path,"a+",encoding='utf-8')as file:
                file.write("y|"+x[1]+'\n')
            
            
    
    sock.close()
        
        
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('127.0.0.1',8888))
s.listen(5)
while True:
    sock,addr=s.accept()
    t=threading.Thread(target=tcplink,args=(sock,addr))
    t.start()
    
