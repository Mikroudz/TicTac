from peli import Game
from ai import Ai
import os

computer = Ai()
tictac = Game()
tictac.drawArea()
validrange = range(0,2)

while 1:
    if tictac.turn == 'o':
        print(tictac.turn + ":n vuoro",end="")
        nextMove = list(input())
        tictac.doMove(int(nextMove[0]), int(nextMove[1]))
    else:
        nextMove = computer.makeBestMove(tictac.gameStatus)
        nextMove = list(nextMove)
        tictac.doMove(int(nextMove[0]), int(nextMove[1]))
    tictac.drawArea()
    if tictac.checkWin() != None:
        print(tictac.checkWin() + " voitti!")
        exit()
