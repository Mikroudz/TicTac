import os

class Game():
    def __init__(self):
        self.area = 0
        self.gameStatus = [['','x','o'],
                           ['x','','o'],
                           ['x','x','x']]
        self.whoseturn = False

    def turn(self):
        return 'x' if self.whoseturn == True else 'o'

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
                self.gameStatus[x][y] = self.turn()
                self.whoseturn = not self.whoseturn
                return self.gameStatus
            else:
                tempArr = self.gameStatus
                tempArr[x][y] = self.turn()
                return tempArr
        else:
            return False

    def checkWin(self):
        for i in range(3):
            for j in range(3):
                self.gameStatus[i][j]

tictac = Game()

tictac.drawArea()
while 1:
    print(str(Game.turn) + " :",end="")
    nextMove = list(input())
    tictac.doMove(int(nextMove[0]), int(nextMove[1]))
    tictac.drawArea()
