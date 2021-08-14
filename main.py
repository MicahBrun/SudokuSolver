import numpy as np

class board():
    def __init__(self, size=3, filledSquares = []):
        self.size = size
        self.boardArr = np.zeros(size^2,size^2)

        for square in filledSquares:
            self.boardArr[square[0],square[1]] = square[2]
        
    def changeSquare(self, square):
        self.boardArr[square[0],square[1]] = square[2]




