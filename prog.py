from peli import Game
from ai import Ai
from tcp_client import Resend
#import kuvantunnistus
from datetime import datetime
import paho.mqtt.client as mqtt
import os
import json

status = "game/tictac/status"
move = "game/tictac/move"
gamestatus = "game/tictac/gamestatus"

#computer = Ai()
client = mqtt.Client("neekeri")
robotTCP = Resend()

try:
    client.connect("127.0.0.1")
except:
    print("MQTT connection failed :(")

try:
    robotTCP.TCPconnect('192.168.100.10', 30002)
except:
    print("Cannot connect to robot")

client.publish(status, "Game start")
tictac = Game(False)
tictac.drawArea()
client.publish(gamestatus, json.dumps(tictac.gameStatus))

validrange = range(0,2)
executionTime = 0

while 1:
    if tictac.turn == 'o':
        print(tictac.turn + ":n vuoro",end="")
        client.publish(status, tictac.turn + ":n vuoro")
        nextMove = list(input())
        tictac.doMove(int(nextMove[0]), int(nextMove[1]))
    else:
        client.publish(status, tictac.turn + ":n vuoro")

        startTime = datetime.now()
        computer = Ai()
        nextMove = computer.makeBestMove(tictac.gameStatus)
        executionTime = datetime.now() - startTime
        nextMove = list(nextMove)
        tictac.doMove(int(nextMove[0]), int(nextMove[1]))
        robotTCP.TCPsend(nextMove[0],nextMove[1])

        del computer
    client.publish(gamestatus, json.dumps(tictac.gameStatus))
    tictac.drawArea()

    print(executionTime)
    if tictac.checkWin() != None:
        print(tictac.checkWin() + " voitti!")
        client.publish(status, tictac.checkWin() + " voitti!")
        exit()
    elif not tictac.isEmptyPlaces():
        print("Kukaan ei voittanu :(")
        client.publish(status, "Kukaan ei voittanut")
        exit()
