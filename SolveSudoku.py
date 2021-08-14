import main
import numpy as np

def int2bmtuple(n,m=9):
    #converts an integer into a tuple represeenting its digits in base 9
    bm = np.array([0,0,0])
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
    cover = np.zeros((4*(size**2)**2+1,(size**2)**3),dtype=int) #row is the constraint sets, column is the possibility (row,column,num)
    for i in range((size**2)**3): #The final row will store the initial index
        cover[4*(size**2)**2,i] = i

    
    #sets the members of all the sets under restrictions row-column, column-number, number-row
    tEle=np.array([0,0,0])
    for a in range(2):
        for i in range(size**2):
            tEle[a] = i
            for j in range(size**2):
                tEle[(a+1)%3] = j
                for k in range(size**2):
                    tEle[(a+2)%3] = k

                    nEle = bmtuple2int(tEle)
                    nSet = bmtuple2int(np.array([a,i,j]))
                    cover[nSet,nEle] = 1
    
    #sets the members for the box restrictions
    for i1 in range(size):
        for j1 in range(size):
            for i2 in range(size):
                for j2 in range(size):
                    for n in range(size**2):
                        nEle = bmtuple2int([size*i1+i2,size*j1+j2,n])
                        nSet = bmtuple2int([3,3*i1+j1,n])
                        cover[nSet,nEle] = 1

    return cover

#def deleteOtherCol

def algorithmX(cover, reqLst=[[]]):
    shape = cover.shape

