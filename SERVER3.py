from tkinter import *
import socket
import requests
import os
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import random

root=Tk()
root.geometry("305x600")
root.resizable(False,False)
root.title("File Sharing GUI App")

frame=Frame(root)
frame.pack()

host_name=Label(frame,text="HOST NAME: "+socket.gethostname(),font=("Arial", 13,"bold"),bg="lightblue",fg="darkblue")
host_name.pack(ipadx=80,fill=BOTH)

ip_name=Label(frame,text="IP ADDRESS: "+socket.gethostbyname(socket.gethostname()),font=("Arial", 13,"bold"),bg="lightblue",fg="darkblue")
ip_name.pack(ipadx=80,fill=BOTH)

file_list=Listbox(root,bg="lightgrey",width=20)
file_list.pack(ipadx=90)


note=Label(root,text="Wait Checking Your Connectivity...",bg="black",fg="green",font=("Arial",10,"bold"))
note.pack(ipadx=150)


url="https://google.com"
timeout=5
try:
	request = requests.get(url, timeout=timeout)
	note.config(text="Online")
except (requests.ConnectionError, requests.Timeout) as exception:
    note.config(fg="red",text="Offline")
    ip_name.configure(padx=19)   

def add():
    global filename
    filename = filedialog.askopenfilename()
    c=str(filename)
    name=os.path.basename(filename)
    if bool(c) is True:
        box.configure(fg="green")
        file_list.insert(END,name)
        box.insert(END,"File Added Succesfully......\n")
    else:
        box.insert(END,"File Not Selected ......\n")

    


    

def remove():
    file_list.delete(ACTIVE)


def send():

    messagebox.showinfo("Ready To Send....", "Type address or Host name From Reciever Side")
    
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostname(),1234))
    s.listen(1)
    print(socket.gethostname())  
    try:
        cli,adr=s.accept()
        box.insert(END,"Waiting For Connection....\n")
        box.insert(END,"Connected Succesfully To: "+str(adr) + "\n")
    except socket.error as error:
        box.insert(END,str(error))
    file_s=filename
    a=os.path.getsize(file_s)
    name,exte=os.path.splitext(file_s)
    b=str(a)
    cli.send(bytes(exte,"utf-8"))

    print(a)  
    cli.send(bytes(b,"utf-8"))
    f=open(file_s,"rb")
    data=f.read(a)
    while data:
        cli.send(data)
        data=f.read(a)
        f.close()
        box.insert(END,"File Transfered Succesfully To: " +str(socket.gethostname())+"\n")



def rec():
    ip=simpledialog.askstring("RECIEVER ADDDRESS","ENTER HOST NAME OR IP ADDRESS: ",parent=root)
    
    
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host=ip
    try:
        s.connect((host,1234))
        box.insert(END,"Succesfully Connected With: "+str(host)+"\n")
    except socket.error as error:
        box.insert(END,str(error))

    directory="PyShare"
    parent_dir="D:/"

    ext=s.recv(10000)
    exte=ext.decode("utf-8")
    print(exte)

    msg=s.recv(100000)
    a=msg.decode("utf-8")
    print(a)
    b=int(a)  
    file_name=simpledialog.askstring("FILENAME","NAME OF RECIEVED FILE:",parent=root)

    if file_name is not None:     
        file_s=str(file_name+str(exte))
        path = os.path.join(parent_dir,directory)
        try:  
            os.mkdir(path)  
        except OSError as error:  
            print("\n")
        save=os.path.join(path,file_s)
        f=open(save,"wb")
        data=s.recv(b,socket.MSG_WAITALL)
        f.write(data)
        f.close()
        box.insert(END,"Your File Is Recieved At: D://PyShare//"+str(file_s)+"\n")
    else:
        name2=str(random.randrange(1,50641206))
        file_s=str(name2+str(exte))
        path = os.path.join(parent_dir,directory)
        try:  
            os.mkdir(path)  
        except OSError as error:  
            print("\n")
        save=os.path.join(path,file_s)
        f=open(save,"wb")
        data=s.recv(b,socket.MSG_WAITALL)
        f.write(data)
        f.close()
        box.insert(END,"Your File Is Recieved At: D://PyShare//"+str(file_s)+"\n")








frame1=Frame(root,bg="lightgrey")
frame1.pack()

add=Button(frame1,text="ADD FILES",font=("Arial",10,"bold"),bg="lightgreen",cursor="hand2",command=add)
add.grid(row=4,padx=5,ipadx=35,ipady=30)

remove=Button(frame1,text="REMOVE FILE",font=("Arial",10,"bold"),bg="#fa8e70",cursor="hand2",command=remove)
remove.grid(row=4,column=2,ipadx=15,ipady=30)

send=Button(frame1,text="SEND",font=("Arial",10,"bold"),bg="lightblue",cursor="hand2",command=send)
send.grid(row=5,padx=5,ipadx=52,ipady=30)

rec=Button(frame1,text="RECIEVE",font=("Arial",10,"bold"),bg="yellow",cursor="hand2",command=rec)
rec.grid(row=5,column=2,padx=5,ipadx=32,ipady=30)

box=Text(root,font=("Arial"),height=10,width=50,bg="black",fg="green")
box.pack()

root.mainloop()
