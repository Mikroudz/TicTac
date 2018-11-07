import os

class Game(object):
    def __init__(self):
        self.area = 0

        self.gameStatus = [['','',''],
                           ['','',''],
                           ['','','']]
        self.player = 'o'
        self.opponent = 'x'
        self.turn = self.player
        self.laskin = 0

    def drawArea(self):
        os.system('clear')
        for i in range(3):
            print("\t|", end ='')
            for j in range(3):
                print(" " + (self.gameStatus[i][j] if self.gameStatus[i][j] != "" else " ") + " |", end ='')
            print("\n")

    def doMove(self, x, y, saveMove = True):
        if self.gameStatus[x][y] == "":
            if saveMove:
                self.gameStatus[x][y] = self.turn
                self.turn = self.player if self.turn == self.opponent else self.opponent
                return self.gameStatus
            else:
                tempArr = self.gameStatus
                tempArr[x][y] = self.turn
                return tempArr
        else:
            return False

    def checkWin(self, peliArr = []):
        #import pdb; pdb.set_trace()
        if len(peliArr) < 1:
            peliArr = self.gameStatus
        for i in range(3):
            if peliArr[i][0] != "":
                if peliArr[i][0] == peliArr[i][1] and peliArr[i][1] == peliArr[i][2]:
                    return peliArr[i][0]
            if peliArr[0][i] != "":
                if peliArr[0][i] == peliArr[1][i] and peliArr[1][i] == peliArr[2][i]:
                    return peliArr[0][i]
        if peliArr[1][1] != "":
            if peliArr[0][0] == peliArr[1][1] and peliArr[1][1] == peliArr[2][2]:
                return peliArr[0][0]
            if peliArr[0][2] == peliArr[1][1] and peliArr[1][1] == peliArr[2][0]:
                return peliArr[1][1]
        return None
