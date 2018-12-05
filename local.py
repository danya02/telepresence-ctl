import pygame
pygame.init()
import threading

import socket

class VexRemote():
    def __init__(self):
        self.ip='192.168.1.241'
        self.port=9001
        self.running=True
        self.socksend=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockrecv=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockrecv.bind(('0.0.0.0',self.port))
        self.data=b''
        self.joystick=pygame.joystick.Joystick(0)
        self.joystick.init()
        self.recv_thread = threading.Thread(target=self.recv_loop,daemon=True)
        self.recv_thread.start()
        self.clock=pygame.time.Clock()
        self.joy_thread = threading.Thread(target=self.joystick_loop,daemon=True)
        self.joy_thread.start()

    def send(self,data):
        print(data)
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
        pass
    def tell_rotation_phase(self,left,right):
        self.send(b'r:'+bytes(str(left),'utf-8')+b':'+bytes(str(right),'utf-8'))
    def joystick_loop(self):
        while self.running:
            pygame.event.pump()
            self.clock.tick(10)
            x=self.joystick.get_axis(0)
            y=self.joystick.get_axis(1)
            y=-y
            right=x+y
            left=-x+y
            self.tell_rotation_phase(left,right)

v=VexRemote()

input()
