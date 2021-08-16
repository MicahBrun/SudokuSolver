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
    #Count all the ones and find the first element with the lowest number
    count1s = np.count_nonzero( cover[arrRemainingEle,:][:, arrRemainingSets] , axis = 1 )
    min1sEleIdx = np.argmin(count1s)

    #Give a list of all the elements with this index
    setsWithEle = arrRemainingSets[np.nonzero(cover[min1sEleIdx,arrRemainingSets])[0]]

    return setsWithEle

def getFinalLstEle(lst):
    hold = lst.pop()
    lst.append(hold)
    return hold

def algorithmX(cover, reqLst = []):
    numberOfEle, numberOfSets = cover.shape

    treeLoc = collections.deque([0]) #Will function as a stack with information on the order in the tree one is

    arrRemainingEle = np.arange(numberOfEle)
    arrRemainingSets = np.arange(numberOfSets)
    treeArrs = [[arrRemainingEle,arrRemainingSets]] #Holds the remeining Elements and remaining Sets for each level of the tree, will work like a stack    
    
    treeSetsWithEle = collections.deque([]) #finds the index of the first row (element) with the lowest number of 1s
    setsWithEle = findMinIdxAndEle(cover, arrRemainingEle, arrRemainingSets)
    treeSetsWithEle.append(setsWithEle)

    finalListOfSets = collections.deque([])
    
    while 1:
        #if there are no more elements, so the sets cover all the elements, return the list of sets
        if treeArrs[-1][0].size == 0:
            return finalListOfSets


        #go to next level in tree
        
        

        

        #if the minimum number of 1s is 0 the problem isn't solved
        if setsWithEle.size == 0:

            #goes through the tree, if all branches have been looked at it goes back through the tree until it can find a new branch
            for i in range(len(treeLoc)):
                if treeLoc[-1] < len(treeSetsWithEle[-1]) -1:
                    treeLoc[-1] = treeLoc[-1] +1
                    break
                treeLoc.pop()
                treeSetsWithEle.pop()
                treeArrs.pop()
                finalListOfSets.pop()
            
            setsWithEle = findMinIdxAndEle(cover, treeArrs[-1][0], treeArrs[-1][1])
            #print(finalListOfSets)
        else: #if the minimum number of ones is not 0 continue onto the next level
            setIdx = treeSetsWithEle[-1][ treeLoc[-1] ] #Takes the matrix index of the set that we decided is in the solution
            finalListOfSets.append(setIdx)
            treeArrs.append( removeEleSet(cover, treeArrs[-1][0], treeArrs[-1][1], setIdx) )
            setsWithEle = findMinIdxAndEle(cover, treeArrs[-1][0], treeArrs[-1][1])
            treeSetsWithEle.append(setsWithEle)
            treeLoc.append(0)
        
def lst2Board(lst):
    board = np.zeros((9,9))
    for item in lst:
        t = int2bmtuple(item)
        board[t[0],t[1]] = t[2] +1
    
    return board

def board2Lst(board):
    nonzeros = np.nonzero(board)

    lst=[]
    for i, row in enumerate(noneZero):
        for column in row:
            lst.append( (i,column, board[i,column] ) )
    
    return lst










          
        




