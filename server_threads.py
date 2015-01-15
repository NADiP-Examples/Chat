#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import os, sys, fnmatch
import datetime
host = "192.168.1.170"
port = 12345

#Список рассылки
emailList = ["zz@zz.ru","dd@dd.com"]

#Список клиентов
ListClients = {"localhost":"127.0.0.1"}

now_date = datetime.date.today() # Текущая дата (без времени)
log_path = 'srvMFR_'+now_date.strftime("%d.%m.%Y %I:%M %p")+'.log'


def SendLog(msg):
 myf = open(log_path, 'a')
 now = datetime.date.today() # Текущая дата (без времени)
 myf.write(now.strftime("%d.%m.%Y %I:%M %p")+": "+msg+'\n')
 print(msg)
 myf.close()


def sendEmail(name):
 for email in emailList:
     print("отправка на почту:",email)
     l = os.popen("mail -s '"+name+"' "+email+" < /dev/null").read()
     SendLog(name)
     print(l)

def EchoClients():

 return str(ListClients)


class Connect(threading.Thread):
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        threading.Thread.__init__(self)
        print(self.addr,"...connected")
        ListClients[self.addr] = self.addr
    def run (self):
        while 1:
            try:
                buf = self.sock.recv(2048)
                if (not buf): #если клиент оключился
                      msg = "Server ["+self.addr[0]+"] "+ListClients[self.addr]+":...disconnected"
                      print(msg)
                      sendEmail(msg)
                      break
                print (self.addr,buf)
                     #l = os.popen(buf).read()
                self.sock.send(buf)
                if buf[:5]=="/NAME":
                     OldName = ListClients[self.addr]
                     ListClients[self.addr] = buf[5:].strip()
                     print ("Client ",OldName," now: ",ListClients[self.addr])
                     sendEmail("Client online:"+self.addr[0]+" "+ListClients[self.addr])
                if buf[:4]=="/MSG":
                    print ("Client ",ListClients[self.addr],"say: ",buf[4:].strip() )
                    #SendLog("Client "+ListClients[self.addr]+" say: "+buf[4:].strip())
                    #print self.addr[1]
                if buf[:6]=="/EMAIL":
                   sendEmail("Message from: ["+self.addr[0]+"] "+str(ListClients[self.addr])+buf[6:].strip())
                if buf[:5]=="/LIST":
                    self.sock.send(EchoClients())
                if buf == "exit":
                     sock.send("bye")
                     break
            except socket.error:
               msg = "Server ["+self.addr[0]+"] "+ListClients[self.addr]+":...disconnected"
               print(msg)
               sendEmail(msg)
               del ListClients[self.addr]
               #print "не могу отправить"
               #s.close()
               break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
while True:
    sock, addr = s.accept()
    Connect(sock, addr).start()