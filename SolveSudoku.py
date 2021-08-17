# Micah Brown 2021

from numpy.core.fromnumeric import nonzero
import main
import numpy as np
import collections


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



def createSudokuCover(size=3):


    numberOfSets = (size**2)**3
    numberOfObjects = 4*((size**2)**2)
    sideLength = size**2


    cover = np.zeros( (numberOfObjects, numberOfSets), dtype=int) #row is the constraint sets, column is the possibility (row,column,num)

    #NOTE: FOR THE FOLLOWING CODE INSIDE THIS FUNCTION, ANY MENTION OF 'SET' SHOULD BE 'ELEMENT' AND VICE VERSA

    #sets the members of all the sets under restrictions row-column, column-number, number-row
    tEle=np.array([0,0,0])
    for a in range(3):
        for i in range(sideLength):
            tEle[a] = i
            for j in range(sideLength):
                tEle[(a+1)%3] = j
                for k in range(sideLength):
                    tEle[(a+2)%3] = k

                    nEle = bmtuple2int(tEle)
                    nSet = bmtuple2int(np.array([a,i,j]))
                    cover[nSet,nEle] = 1
    
    #sets the members for the box restrictions
    for i1 in range(size):
        for j1 in range(size):
            for i2 in range(size):
                for j2 in range(size):
                    for n in range(sideLength):
                        nEle = bmtuple2int([size*i1+i2,size*j1+j2,n])
                        nSet = bmtuple2int([3,3*i1+j1,n])
                        cover[nSet,nEle] = 1

    return cover

def removeEleSet(cover, arrRemainingEle, arrRemainingSets, setIdx):
    #Performs the deletion part of Algorithm X which involves deleting all
    #elements that are in a set from our list as well as any set that contains these elements

    corEleWith1 = np.nonzero( cover[arrRemainingEle, setIdx] )[0] #for the given setIdx (column) finds all the elements that are in that set
    for ele in corEleWith1: #for each element that is in the set
        corSetWith1 = np.nonzero( cover[arrRemainingEle[ele],arrRemainingSets])[0] #find all the sets (columns) that contain this element
        arrRemainingSets = np.delete(arrRemainingSets, corSetWith1) #And delete them
    arrRemainingEle = np.delete(arrRemainingEle, corEleWith1) #Then remove all the elements (rows) that are in the set we chose

    return [arrRemainingEle, arrRemainingSets] #return the remaining Elements and Sets in an vector array

def findMinIdxAndEle(cover, arrRemainingEle, arrRemainingSets):
    #Count all the ones and find the first element with the lowest number of ones
    count1s = np.count_nonzero( cover[arrRemainingEle,:][:, arrRemainingSets] , axis = 1 )
    #take the index of this element
    min1sEleIdx = arrRemainingEle[np.argmin(count1s)]

    #Give a list of all the elements with this index
    setsWithEle = arrRemainingSets[np.nonzero(cover[min1sEleIdx,arrRemainingSets])[0]]

    return setsWithEle

def getFinalLstEle(lst):
    hold = lst.pop()
    lst.append(hold)
    return hold

def removeReq(cover, arrRemainingEle,arrRemainingSets, reqlist):

    setIdxLst = [bmtuple2int(reqtup) for reqtup in reqlist]
    for setIdx in setIdxLst:
        [arrRemainingEle, arrRemainingSets] = removeEleSet(cover, arrRemainingEle, arrRemainingSets, setIdx)
        _ = findMinIdxAndEle(cover, arrRemainingEle, arrRemainingSets)
    
    return [arrRemainingEle, arrRemainingSets]


def algorithmX(cover, reqLst = []):
    numberOfEle, numberOfSets = cover.shape

    treeLoc = collections.deque([0]) #Will function as a stack with information on the order in the tree one is

    arrRemainingEle = np.arange(numberOfEle)
    arrRemainingSets = np.arange(numberOfSets)

    [arrRemainingEle, arrRemainingSets] = removeReq(cover, arrRemainingEle, arrRemainingSets, reqLst)

    treeArrs = [[arrRemainingEle,arrRemainingSets]] #Holds the remeining Elements and remaining Sets for each level of the tree, will work like a stack    
    
    treeSetsWithEle = collections.deque([]) #finds the index of the first row (element) with the lowest number of 1s
    setsWithEle = findMinIdxAndEle(cover, arrRemainingEle, arrRemainingSets)
    treeSetsWithEle.append(setsWithEle)

    finalListOfSets = collections.deque([])
    
    #if there are no more elements, so the sets cover all the elements, return the list of sets
    if treeArrs[-1][0].size == 0:
        return finalListOfSets
    
    while 1:        

        #if the minimum number of 1s is 0 the problem isn't solved and we must go back up the tree
        if setsWithEle.size == 0:

            #goes through the tree, if all branches have been looked at it goes back up the tree until it can find a new branch
            for i in range(len(treeLoc)):
                if treeLoc[-1] < len(treeSetsWithEle[-1]) -1:
                    treeLoc[-1] = treeLoc[-1] +1
                    break
                treeLoc.pop()
                treeSetsWithEle.pop()
                treeArrs.pop()
                finalListOfSets.pop()
            
            setsWithEle = findMinIdxAndEle(cover, treeArrs[-1][0], treeArrs[-1][1])

        else: #if the minimum number of ones is not 0 continue onto the next level of Tree
            setIdx = treeSetsWithEle[-1][ treeLoc[-1] ] #Takes the matrix index of the set that we decided is in the solution
            finalListOfSets.append(setIdx)
            treeArrs.append( removeEleSet(cover, treeArrs[-1][0], treeArrs[-1][1], setIdx) )
            if treeArrs[-1][0].size == 0:
                return finalListOfSets
            setsWithEle = findMinIdxAndEle(cover, treeArrs[-1][0], treeArrs[-1][1])
            treeSetsWithEle.append(setsWithEle)
            treeLoc.append(0)

def int2Board(lst):
    board = np.zeros((9,9), dtype=int)
    for item in lst:
        t = int2bmtuple(item)
        board[t[0],t[1]] = t[2] +1
    
    return board

def lst2Board(lst):
    board = np.zeros((9,9), dtype=int)
    for item in lst:
        board[item[0],item[1]] = item[2] +1
    
    return board

def board2Lst(board):
    nonzeros = np.nonzero(board)

    lst=[]
    for i in range(len(nonzeros[0])):
        lst.append( (nonzeros[0][i],nonzeros[1][i],board[ nonzeros[0][i],nonzeros[1][i] ]) )
    
    return lst

