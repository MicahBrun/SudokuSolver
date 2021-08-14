import numpy as np

class board():
    def __init__(self, filledSquares = [], size=3):
        self.size = size

        s = [size**2 for i in range(2)]
        self.boardArr = np.zeros(s, dtype = int)

        for square in filledSquares:
            self.boardArr[square[0],square[1]] = square[2]
        
    def changeSquare(self, square):
        self.boardArr[square[0],square[1]] = square[2]
    
    def isLegal(self):
        #check rows
        arrLen = self.size**2
        for i in range(arrLen):
            subArr = self.boardArr[i,:]
            for n in range(arrLen):
                if np.count_nonzero(subArr == n+1) > 1:
                    return False
        
        #check columns
        for i in range(arrLen):
            subArr = self.boardArr[:,i]
            for n in range(arrLen):
                if np.count_nonzero(subArr == n+1) > 1:
                    return False
        
        #check squares
        for i in range(self.size):
            for j in range(self.size):
                subArr = self.boardArr[self.size*i:self.size*(i+1),self.size*j:self.size*(j+1)]
                for n in range(arrLen):
                    if np.count_nonzero(subArr == n+1) > 1:
                        return False
        
        return True










