from peli import Game
from ai import Ai
from datetime import datetime
import os

#computer = Ai()
tictac = Game()
tictac.drawArea()
validrange = range(0,2)
executionTime = 0

while 1:
    if tictac.turn == 'o':
        print(tictac.turn + ":n vuoro",end="")
        nextMove = list(input())
        tictac.doMove(int(nextMove[0]), int(nextMove[1]))
    else:
        startTime = datetime.now()
        computer = Ai()
        nextMove = computer.makeBestMove(tictac.gameStatus)
        executionTime = datetime.now() - startTime
        nextMove = list(nextMove)
        tictac.doMove(int(nextMove[0]), int(nextMove[1]))
    tictac.drawArea()
    print(executionTime)
    if tictac.checkWin() != None:
        print(tictac.checkWin() + " voitti!")
        exit()
    elif not tictac.isEmptyPlaces():
        print("Kukaan ei voittanu :(")
        exit()
