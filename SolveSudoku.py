import main
import numpy as np

def int2bmtuple(n,m=9):
    #converts an integer into a tuple represeenting its digits in base 9
    bm = [0,0,0]
    bm[0] = n//m//m
    bm[1] = n//m%m
    bm[2] = n%m

    return tuple(bm)

def bmtuple2int(bmtuple,m=9):
    size = len(bmtuple)

    n = 0
    for i in range(size):
        n+=bmtuple[i]*m**(size-1-i)
    
    return n



def createSudokuCover(size):
    cover = np.zeros((4*size**2**2,size**2**3+1),dtype=int) #row is the constraint sets, column is the possibility (row,column,num)
    for i in range(4*size**2**2):
        cover[i,size**2**3] = i
    


    #define row column constraint set (1 number per row column)

