import os
from peli import Game

class Ai(Game):
    def __init__(self):
        self.maximum = False
        self.gameBoard = []
        self.curBestMoveVal = 0
        self.bestX = 0
        self.bestY = 0

    def isEmptyPlaces(self):
        for i in range(3):
            for j in range(3):
                if self.gameBoard[i][j] == "":
                    return True
        return False

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

    def makeBestMove(self,gameBoard):
        self.gameBoard = gameBoard
        for i in range(3):
            for j in range(3):
                if self.gameBoard[i][j] == "":
                    self.gameBoard[i][j] = 'x'
                    bestMove = self.minimax(self.gameBoard, self.maximum)
                    if self.curBestMoveVal < bestMove:
                        self.curBestMoveVal = bestMove
                        self.bestY = j
                        self.bestX = i
        asd = ''
        return str(self.bestY) + str(self.bestX)
