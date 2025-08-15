import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import time
import threading
import socket
import os
f=('Comic Sans MS',)

win=Tk()
win.title("登录页面")
win.geometry("300x150")
win.minsize(300,150)
win.maxsize(300,150)
label=Label(win,text="Hello!",font=f)
label.pack()

name=Label(win,text="用户名")
password=Label(win,text="密码")
namein=Entry(win,width=30)
passwordin=Entry(win,width=30,show='*')

name.place(x=10,y=30)
namein.place(x=65,y=30)
password.place(x=10,y=60)
passwordin.place(x=65,y=60)

#登陆尝试
def login():
    try: 
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('127.0.0.1',8888))
        msg="000|"+namein.get()
        s.send(msg.encode('utf-8'))
    except Exception as e:
        messagebox.showerror("ERROR",e)
    time.sleep(0.7)    
    mess="001|"+namein.get()+"|"+passwordin.get()
    s.send(mess.encode('utf-8'))
    d=s.recv(1024)
    result=d.decode('utf-8')



    
    if result=="PASS":
        #登陆成功主页面
        
        filename=namein.get()+"schat"
        
        script_dir=os.path.dirname(os.path.abspath(__file__))
        user_dir=os.path.join(script_dir,filename)
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
            file_path=os.path.join(user_dir,"friendlist.txt")
            with open(file_path,"w") as file:
                pass
        
        win2=Tk()
        yourname=namein.get()
        win.destroy()
        win2.title(yourname+"的小QQ")
        win2.geometry("300x500")
        win2.minsize(300,500)
        win2.maxsize(300,500)

        localbuffer002=[]
        localbuffer004=[]
        #创建线程接受信息并写入文件（未实现）
        def receive(sock1):
            while True:
                mes=sock1.recv(1024)
                y=mes.decode('utf-8').split('|')
                if(y[0]=="xxx"):
                    continue
                if(y[0]=="xx2"):
                    localbuffer002.append(y[1])
                #xx3开头代表要加载的云端聊天记录
                if(y[0]=="xx3"):
                    p="with"+y[1]+".txt"
                    script_dir=os.path.dirname(os.path.abspath(__file__))
                    user_dir=os.path.join(script_dir,yourname+"schat")
                    file_path=os.path.join(user_dir,p)
                    try:
                        chatlist=open(file_path,"a+",encoding='utf-8')
                        messxx3=y[1]+":"+y[2]+'\n'+y[3].strip()+'\n'
                        chatlist.write(messxx3)
                        chatlist.flush()
                        chatlist.close
                    except Exception as e:
                        print(e)
                if(y[0]=="xx4"):
                    localbuffer004.append(y[1])
                if(y[0]=="xx5"):
                    print(y)
                    p="friendlist.txt"
                    p2="with"+y[2].strip()+".txt"
                    script_dir=os.path.dirname(os.path.abspath(__file__))
                    user_dir=os.path.join(script_dir,yourname+"schat")
                    file_path=os.path.join(user_dir,p)
                    file_path2=os.path.join(user_dir,p2)
                    if y[1]=="x":
                        print("add")
                        if not os.path.exists(file_path2):
                            with open(file_path2,"w",encoding='utf-8')as file:
                                pass
                        with open(file_path,"a+",encoding='utf-8')as file:
                            file.write(y[2].strip()+'\n')
                            print("add_success")
                            file.flush()
                    if y[1]=="y":
                        print("delete")
                        
                        lines=[]
                        with open(file_path,"r+",encoding='utf-8')as file:    
                            for line in file:
                                if line.strip()==y[2].strip() or line.strip()=="":
                                    print("findit")
                                    continue
                                lines.append(line)
                        with open(file_path,"w+",encoding='utf-8')as file:
                            for line in lines:
                                file.write(line)
                                print("delete_success")
                            file.flush()
                                
                            
                                
                    
                
                    
                
                    
                    
        threading.Thread(target=receive,args=(s,),daemon=True).start()            




        #头像（未实现）
        tou=Label(win2,bitmap='question')
        tou.place(x=30,y=30)

        f1=LabelFrame(win2,height=10,width=265,text="好友列表")
        f1.place(x=20,y=80)



        def chat(event):
            #聊天框
            win3=Tk()
            friendname=friendlist.get(friendlist.curselection())
            win3.title("这是一个和"+friendname+"的聊天框")
            win3.geometry("500x500")
            
            msgedit=Entry(win3,width=50)
            msgedit.place(x=30,y=450)

            
            def send():
                textbox.config(state=NORMAL)
                message=msgedit.get()
                msgedit.delete(0,END)
                
                mess="002|"+message+"|"+friendname+"|"+yourname
                s.send(mess.encode('utf-8'))
                while len(localbuffer002)==0:
                    time.sleep(0.5)
                result=localbuffer002[0]
                del localbuffer002[0]
                    
                if not result:
                    result="未知错误"
                
                #textbox.insert(END,"我:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"|"+result+'\n',"green")
                #textbox.insert(END,message+'\n')
                p="with"+friendname+".txt"
                script_dir=os.path.dirname(os.path.abspath(__file__))
                user_dir=os.path.join(script_dir,yourname+"schat")
                file_path=os.path.join(user_dir,p)
                
                with open(file_path,"a+",encoding='utf-8') as file:
                    file.write("我:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"|"+result+'\n')
                    file.write(message+'\n')
                    file.flush()
                
                textbox.update()
                textbox.config(state=DISABLED)
                textbox.see(END)


                
            def send_enter(event):
                send()
            
            #发送键
            sendbutton=Button(win3,width=6,text="发送",command=send)
            sendbutton.place(x=420,y=445)

            textbox=scrolledtext.ScrolledText(win3,width=63,height=30)
            

            #聊天记录文件同步到消息框
            def update():
                p="with"+friendname+".txt"
                script_dir=os.path.dirname(os.path.abspath(__file__))
                user_dir=os.path.join(script_dir,yourname+"schat")
                file_path=os.path.join(user_dir,p)
                if not os.path.exists(file_path):
                    with open(file_path,'w',encoding='utf-8',newline='') as file:
                        pass 
                fileline=0
                while True:
                    time.sleep(0.5)
                    
                    with open(file_path,'r',encoding='utf-8') as file:
                        lines=file.readlines()
                    num_lines=len(lines)
                    textbox.tag_configure("green", foreground="green")
                    textbox.tag_configure("blue", foreground="blue")
                    while fileline<num_lines:
                        textbox.config(state=NORMAL)
                        color="blue"
                        name=lines[fileline].split(':')[0]
                        if name=="我":
                            color="green"
                        
                        textbox.insert(END,lines[fileline],color)
                        textbox.insert(END,lines[fileline+1])
                        fileline=fileline+2
                        textbox.config(state=DISABLED)
                        textbox.see(END)
            threading.Thread(target=update,daemon=True).start()
            textbox.config(state=DISABLED)
            textbox.place(x=30,y=30)
            

            
            win3.bind("<Return>",send_enter)
            win3.mainloop()
        
        friendlist=Listbox(f1,height=20,width=33)

        
        def update_friendlist():
            friendlist.update()
            now_friendlist=[]
            p2="friendlist.txt"
            script_dir=os.path.dirname(os.path.abspath(__file__))
            user_dir=os.path.join(script_dir,yourname+"schat")
            file_path2=os.path.join(user_dir,p2)
            while True:
                friendlist.update()
                with open(file_path2,"r+",encoding='utf-8')as file:
                    lines=file.readlines()
                if now_friendlist!=lines:
                    now_friendlist=lines
                    for item in now_friendlist:
                        friendlist.insert(END,item.strip())
                    if now_friendlist==[]:
                        friendlist.delete(0,END)
                    friendlist.update()
                time.sleep(1)
                
        threading.Thread(target=update_friendlist,daemon=True).start() 
        scroll=Scrollbar(f1)
        scroll.pack(side=RIGHT,fill=Y)
        scroll.config(command=friendlist.yview())
        friendlist.configure(yscrollcommand=scroll.set)
        friendlist.bind('<Double-1>',chat)




        def show_menu(event):
            menu.post(event.x_root,event.y_root)

        def del_chat():#处理本地文档即可
            p="with"+friendlist.get(friendlist.curselection())+".txt"
            script_dir=os.path.dirname(os.path.abspath(__file__))
            user_dir=os.path.join(script_dir,yourname+"schat")
            file_path=os.path.join(user_dir,p)
            with open(file_path,"w",encoding='utf-8'):
                pass
        #删除好友：发送处理请求（已），本地friendlist文件减少一行（已）
        def del_fri():
            mess005="005|"+yourname+"|"+friendlist.get(friendlist.curselection())
            s.send(mess005.encode('utf-8'))
            
            p="with"+friendlist.get(friendlist.curselection())+".txt"
            p2="friendlist.txt"
            script_dir=os.path.dirname(os.path.abspath(__file__))
            user_dir=os.path.join(script_dir,yourname+"schat")
            file_path=os.path.join(user_dir,p)
            file_path2=os.path.join(user_dir,p2)
            lines=[]
            with open(file_path2,"r",encoding='utf-8')as file:
                lines=file.readlines()
                for line in lines:
                    if line.strip()!=friendlist.get(friendlist.curselection()):
                        lines.append(line.strp())
            with open(file_path2,"w",encoding='utf-8')as file:
                for line in lines:
                    file.write(line)
                    

            
            
            friendlist.delete(friendlist.curselection())
            os.remove(file_path)
            friendlist.update()
         
        menu=Menu(win2,tearoff=0)
        menu.add_command(label="删除聊天记录",command=del_chat)
        menu.add_command(label="删除好友",command=del_fri)
        friendlist.bind('<ButtonRelease-3>',show_menu)        
        friendlist.pack()

        menu2=Menu(win2)
        #添加好友:发送处理请求（已），创建with文档（已）,friendlist文件添加一行（已）
        def add_fri():
            add_friendwin=Toplevel(win2)
            add_friendwin.title("添加好友")
            add_friendwin.geometry("300x140")
            add_label=Label(add_friendwin,text="请输入好友的ID")
            add_label.pack(pady=5)
            add_text=Entry(add_friendwin,width=30)
            add_text.pack(pady=10)
            def confirm():
                add_name=add_text.get()
                p2="friendlist.txt"
                script_dir=os.path.dirname(os.path.abspath(__file__))
                user_dir=os.path.join(script_dir,yourname+"schat")
                file_path2=os.path.join(user_dir,p2)
                with open(file_path2,"r+",encoding='utf-8')as file:
                    lines=file.readlines()
                    for line in lines:
                        if line.strip()==add_name:
                            messagebox.showerror("Error！",add_name+"已经是你的好友咯！")
                            return

                mess004="004|"+yourname+"|"+add_name
                s.send(mess004.encode('utf-8'))
                while len(localbuffer004)==0:
                    time.sleep(0.5)
                result=localbuffer004[0]
                del localbuffer004[0]
                if result=="添加成功":
                    
                    p="with"+add_name+".txt"
                    p2="friendlist.txt"
                    script_dir=os.path.dirname(os.path.abspath(__file__))
                    user_dir=os.path.join(script_dir,yourname+"schat")
                    file_path=os.path.join(user_dir,p)
                    file_path2=os.path.join(user_dir,p2)
                    with open(file_path,"w",encoding='utf-8')as file:
                        pass
                    with open(file_path2,"a+",encoding='utf-8')as file:
                        file.write(add_name+'\n')
                    
                        
                    
                    messagebox.showinfo("恭喜！",result)
                else:
                    messagebox.showerror("Error！",result)
                    
                
            
            add_button=Button(add_friendwin,text="确定",width=10,command=confirm)
            add_button.pack(pady=10)
        menu2.add_command(label="添加好友",command=add_fri)
        win2['menu']=menu2



        
        win2.mainloop()
    else:
        messagebox.showerror("ERROR","用户名或密码错误")

    s.close()

#注册 ：生成user目录下用户目录，拥有friendlist文件（已实现）    
def zhuce():
    try: 
        s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s1.connect(('127.0.0.1',8888))
        msg="000|"+namein.get()
        s1.send(msg.encode('utf-8'))
    except Exception as e:
        messagebox.showerror("ERROR",e)
    time.sleep(0.7)    
    mess="100|"+namein.get()+"|"+passwordin.get()
    s1.send(mess.encode('utf-8'))
    d=s1.recv(1024)
    result=d.decode('utf-8')
    if result=="注册成功" :
        filename=namein.get()+"schat"
        
        script_dir=os.path.dirname(os.path.abspath(__file__))
        user_dir=os.path.join(script_dir,filename)
        os.mkdir(user_dir)
        file_path=os.path.join(user_dir,"friendlist.txt")
        with open(file_path,"w") as file:
            pass
            
        messagebox.showinfo("恭喜！",result)
    else:
        messagebox.showerror("ERROR",result)
    
    s1.close()
        
def login_enter(event):
    login()

log=Button(win,width=10,text="登录",command=login)
log.place(x=40,y=100)
zhuce=Button(win,width=10,text="注册",command=zhuce)
zhuce.place(x=165,y=100)
win.bind("<Return>",login_enter)


win.mainloop()
