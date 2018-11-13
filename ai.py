import os
from peli import Game


class Ai(Game):
    def __init__(self):
        self.curBestMoveVal = -9999
        self.bestX = 0
        self.bestY = 0
        self.gameStatus = []
        self.debug = []

    def minimax(self, tempGameStatus, iters, isMaximizing, alpha, beta):
        gameWinner = self.checkWin(tempGameStatus)
        if gameWinner == 'x':
            return 10-iters
        elif gameWinner == 'o':
            return iters-10

        if not self.isEmptyPlaces():
            return 0

        if isMaximizing:
            bestPlaceScore = -9999
            for i in range(3):
                for j in range(3):
                    if tempGameStatus[i][j] == "":
                        tempGameStatus[i][j] = 'x'
                        bestPlaceScore = max(bestPlaceScore, self.minimax(tempGameStatus, iters, not isMaximizing, alpha, beta))
                        tempGameStatus[i][j] = ""
                        if alpha < bestPlaceScore:
                            alpha = bestPlaceScore
                        if alpha >= beta:
                            break
            return bestPlaceScore
        else:
            bestPlaceScore = 9999
            for i in range(3):
                for j in range(3):
                    if tempGameStatus[i][j] == "":
                        tempGameStatus[i][j] = 'o'
                        bestPlaceScore = min(bestPlaceScore, self.minimax(tempGameStatus, iters, not isMaximizing, alpha, beta))
                        tempGameStatus[i][j] = ""
                        if beta > bestPlaceScore:
                            beta = bestPlaceScore
                        if alpha >= beta:
                            break
            return bestPlaceScore

    def makeBestMove(self,boardStatus):
        self.gameStatus = boardStatus
        for i in range(3):
            for j in range(3):
                if self.gameStatus[i][j] == "":
                    self.gameStatus[i][j] = 'x'
                    self.maximum = False
                    bestMove = self.minimax(self.gameStatus, 0, self.maximum, -1000, 1000)
                    self.debug.append([i, j, bestMove])
                    self.gameStatus[i][j] = ""
                    if self.curBestMoveVal < bestMove:
                        self.curBestMoveVal = bestMove
                        self.bestY = i
                        self.bestX = j
        #self.debug.append([self.bestY,self.bestX])
        #import pdb; pdb.set_trace()
        return str(self.bestY) + str(self.bestX)
