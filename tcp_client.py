#!/usr/bin/env python
import socket
from peli import Game

class Resend(object):
    def __init__(self):
        self.HOST = None
        self.PORT = None
        self.BUFFER_SIZE = 1024
        self.s = None
        #lisää tää programmiin
        #if tictac.doMove != False:
            #TCP.TCPsend(nextMove[0],nextMove[1])

    def __del__(self):
        self.s.close()

    def TCPsend(self, x, y):
        self.s.send(self.vert(x, y).encode())
        data = self.s.recv(1024)

    def TCPconnect(self, ip, port):
        self.HOST = ip
        self.PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST,self.PORT))


    def vert(self, x, y):
        if x == '0' and y == '0':
            return "set_digital_out(1,True)\n"
        if x == '0' and y == '1':
            return "set_digital_out(2,True)\n"
        if x == '0' and y == '2':
            return "set_digital_out(3,True)\n"
        elif x == '1' and y == '0':
            return "set_digital_out(4,True)\n"
        if x == '1' and y == '1':
            return "set_digital_out(5,True)\n"
        elif x == '1' and y == '2':
            return "set_digital_out(6,True)\n"
        if x == '2' and y == '0':
            return "set_digital_out(7,True)\n"
        elif x == '2' and y == '1':
            return "set_digital_out(1,True)\n" + "set_digital_out(2,True)\n"
        if x == '2' and y == '2':
            return "set_digital_out(1,True)\n" + "set_digital_out(3,True)\n"
        else:
            print("JOO EI!")
