from peli import Game
from ai import Ai
import os


tictac = Game()
tictac.drawArea()
validrange = range(0,2)
while 1:
    print(tictac.turn + ":n vuoro",end="")
    nextMove = list(input())
    tictac.doMove(int(nextMove[0]), int(nextMove[1]))
    tictac.drawArea()
    if tictac.checkWin() != None:
        print(tictac.checkWin() + " voitti!")
        exit()
