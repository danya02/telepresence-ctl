import threading
import socket
import gpiozero
class VexBot:
    def __init__(self):
        self.sright=gpiozero.Servo(21)
        self.sleft=gpiozero.Servo(20)
        self.ip='192.168.1.255'
        self.port=9001
        self.running=True
        self.socksend=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockrecv=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockrecv.bind(('0.0.0.0',self.port))
        self.data=b''
        self.recv_thread = threading.Thread(target=self.recv_loop,daemon=True)
        self.recv_thread.start()
    def send(self,data):
        self.socksend.sendto(data+b'\n',(self.ip,self.port))
    def recv_loop(self):
        while self.running:
            data,addr = self.sockrecv.recvfrom(16)
            self.data+=data
            data=self.data.split(b'\n')
            for i in data[:-1]: 
                self.callback(i)
            self.data=data[-1]
    def callback(self,data):
        print(data,self.data)
        if data[0]==b'r':
            d,l,r=data.split(b':')
            l=float(str(l,'utf-8'))
            r=float(str(r,'utf-8'))
            self.sleft.value=l
            self.sright.value=r
            if l==r==0:self.stop()


    def forward(self,value=1):
        self.sright.value=-value
        self.sleft.value=-value
    def back(self,value=1):
        self.sright.value=value
        self.sleft.value=value
    def left(self,value=1):
        self.sright.value=-value
        self.sleft.value=value
    def right(self,value=1):
        self.sright.value=value
        self.sleft.value=-value
    def stop(self):
        self.sright.detach()
        self.sleft.detach()

if __name__=='__main__':
    v=VexBot()
    while 1:
        a=input('>')
        if a=='w':v.forward()
        if a=='s':v.back()
        if a=='a':v.left()
        if a=='d':v.right()
        if a=='':v.stop()
