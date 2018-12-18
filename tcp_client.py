#!/usr/bin/env python
import socket
from peli import Game

class resend(Game):
    def __init__(self):
        self.HOST = '192.168.100.10'
        self.PORT = 30002
        self.BUFFER_SIZE = 1024

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #lisää tää programmiin
        #if tictac.doMove != False:
            #TCP.TCPsend(nextMove[0],nextMove[1])

    def TCPsend(self, x, y):


        self.s.connect((self.HOST,self.PORT))

        self.vert(x, y)



        data = self.s.recv(1024)
        self.s.close()


    def vert(self, x, y):



        if x == '0' and y == '0':
            self.s.send (b"set_digital_out(1,True)\n" )
        if x == '0' and y == '1':
            self.s.send (b"set_digital_out(2,True)\n" )
        if x == '0' and y == '2':
            self.s.send (b"set_digital_out(3,True)\n" )
        elif x == '1' and y == '0':
            self.s.send (b"set_digital_out(4,True)\n" )
        if x == '1' and y == '1':
            self.s.send (b"set_digital_out(5,True)\n" )
        elif x == '1' and y == '2':
            self.s.send (b"set_digital_out(6,True)\n" )
        if x == '2' and y == '0':
            self.s.send (b"set_digital_out(7,True)\n" )
        elif x == '2' and y == '1':
            self.s.send (b"set_digital_out(1,True)\n" )
            self.s.send (b"set_digital_out(2,True)\n" )
        if x == '2' and y == '2':
            self.s.send (b"set_digital_out(1,True)\n" )
            self.s.send (b"set_digital_out(3,True)\n" )
        else:
            print("JOO EI!")
