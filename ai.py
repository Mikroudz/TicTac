import os
from peli import Game


class Ai(Game):
    def __init__(self):
        self.maximum = False
        self.curBestMoveVal = -9999
        self.bestX = 0
        self.bestY = 0
        self.gameStatus = []

    def minimax(self, tempGameStatus, isMaximizing):
        gameWinner = self.checkWin(tempGameStatus)
        if gameWinner == 'x':
            return 10
        elif gameWinner == 'o':
            return -10

        if not self.isEmptyPlaces():
            return 0

        if isMaximizing:
            bestPlaceScore = -9999
            for i in range(3):
                for j in range(3):
                    if tempGameStatus[i][j] == "":
                        tempGameStatus[i][j] = 'x'
                        bestPlaceScore = max(bestPlaceScore, self.minimax(tempGameStatus,not self.maximum))
                        tempGameStatus[i][j] = ""
            return bestPlaceScore
        else:
            bestPlaceScore = 9999
            for i in range(3):
                for j in range(3):
                    if tempGameStatus[i][j] == "":
                        tempGameStatus[i][j] = 'o'
                        bestPlaceScore = min(bestPlaceScore, self.minimax(tempGameStatus,not self.maximum))
                        tempGameStatus[i][j] = ""
            return bestPlaceScore

    def makeBestMove(self,boardStatus):
        self.gameStatus = boardStatus
        for i in range(3):
            for j in range(3):
                if self.gameStatus[i][j] == "":
                    self.gameStatus[i][j] = 'x'
                    bestMove = self.minimax(self.gameStatus, self.maximum)
                    self.gameStatus[i][j] = ""
                    if self.curBestMoveVal < bestMove:
                        self.curBestMoveVal = bestMove
                        self.bestY = i
                        self.bestX = j
        #import pdb; pdb.set_trace()
        return str(self.bestY) + str(self.bestX)
