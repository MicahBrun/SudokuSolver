# Micah Brown 2021

from numpy.core.fromnumeric import nonzero
import numpy as np
import collections


def int_to_base_9(n):
    # converts an integer into a tuple represeenting its digits in base 9
    BASE = 9

    bm = np.array([0, 0, 0])
    bm[0] = n // BASE // BASE
    bm[1] = n // BASE % BASE
    bm[2] = n % BASE

    return tuple(bm)


def base_9_to_int(bmtuple):
    BASE = 9

    size = len(bmtuple)

    n = 0
    for i in range(size):
        n += bmtuple[i] * BASE ** (size - 1 - i)

    return n


def create_sudoku_cover(size=3):

    number_of_sets = (size ** 2) ** 3
    number_of_elements = 4 * ((size ** 2) ** 2)
    sideLength = size ** 2

    cover = np.zeros(
        (number_of_elements, number_of_sets), dtype=int
    )  # row is the constraint sets, column is the possibility (row,column,num)

    # NOTE: FOR THE FOLLOWING CODE INSIDE THIS FUNCTION, ANY MENTION OF 'SET' SHOULD BE 'ELEMENT' AND VICE VERSA
    # sets the members of all the sets under restrictions row-column, column-number, number-row
    tEle = np.array([0, 0, 0])
    for a in range(3):
        for i in range(sideLength):
            tEle[a] = i
            for j in range(sideLength):
                tEle[(a + 1) % 3] = j
                for k in range(sideLength):
                    tEle[(a + 2) % 3] = k

                    nEle = base_9_to_int(tEle)
                    nSet = base_9_to_int(np.array([a, i, j]))
                    cover[nSet, nEle] = 1

    # sets the members for the box restrictions
    for i1 in range(size):
        for j1 in range(size):
            for i2 in range(size):
                for j2 in range(size):
                    for n in range(sideLength):
                        nEle = base_9_to_int([size * i1 + i2, size * j1 + j2, n])
                        nSet = base_9_to_int([3, 3 * i1 + j1, n])
                        cover[nSet, nEle] = 1

    return cover


def give_elements_and_sets_after_deletion(
    cover, remaining_elements, remaining_sets, setIdx
):
    # Performs the deletion part of Algorithm X which involves deleting all
    # elements that are in a set from our list as well as any set that contains these elements

    corEleWith1 = np.nonzero(cover[remaining_elements, setIdx])[
        0
    ]  # for the given setIdx (column) finds all the elements that are in that set
    for ele in corEleWith1:  # for each element that is in the set
        corSetWith1 = np.nonzero(cover[remaining_elements[ele], remaining_sets])[
            0
        ]  # find all the sets (columns) that contain this element
        remaining_sets = np.delete(remaining_sets, corSetWith1)  # And delete them
    remaining_elements = np.delete(
        remaining_elements, corEleWith1
    )  # Then remove all the elements (rows) that are in the set we chose

    return [
        remaining_elements,
        remaining_sets,
    ]  # return the remaining Elements and Sets in an vector array


def give_sets(cover, remaining_elements, remaining_sets):
    # Count all the ones and find the first element with the lowest number of ones
    count1s = np.count_nonzero(cover[remaining_elements, :][:, remaining_sets], axis=1)
    # take the index of this element
    least_covered_element_index = remaining_elements[np.argmin(count1s)]

    # Give a list of all the sets with this index
    sets_containing_least_covered_element = remaining_sets[
        np.nonzero(cover[least_covered_element_index, remaining_sets])[0]
    ]

    return sets_containing_least_covered_element


def removeReq(cover, remaining_elements, remaining_sets, reqlist):

    setIdxLst = [
        base_9_to_int(sudoku_position_and_value)
        for sudoku_position_and_value in reqlist
    ]
    for setIdx in setIdxLst:
        [remaining_elements, remaining_sets] = give_elements_and_sets_after_deletion(
            cover, remaining_elements, remaining_sets, setIdx
        )
        _ = give_sets(cover, remaining_elements, remaining_sets)

    return [remaining_elements, remaining_sets]


class AlgorithmXTree:
    def __init__(self, initial_elements, initial_sets, initial_sets_with_element):

        self.location = collections.deque()
        self.location.append(0)
        self.surviving_elements_tree = [initial_elements]
        self.surviving_sets_tree = [initial_sets]

        self.sets_containing_least_covered__element_tree = [initial_sets_with_element]
        self.current_cover_sets = collections.deque()
        self.current_cover_sets.append(self.give_current_set())

    def give_sets_with_least_covered_element(self):
        return self.sets_containing_least_covered__element_tree[-1]

    def give_surviving_sets(self):
        return self.surviving_sets_tree[-1]

    def give_surviving_elements(self):
        return self.surviving_elements_tree[-1]

    def give_branch_position(self):
        return self.location[-1]

    def number_of_unchecked_sets_with_element(self):
        return len(self.give_sets_with_least_covered_element())

    def go_up_a_layer(self):
        self.location.pop()
        self.surviving_elements_tree.pop()
        self.surviving_sets_tree.pop()
        self.sets_containing_least_covered__element_tree.pop()
        self.current_cover_sets.pop()

    def is_not_on_final_branch(self):
        return (
            self.give_branch_position()
            < self.number_of_unchecked_sets_with_element() - 1
        )

    def increment_branch_position(self):
        self.location[-1] += 1

    def give_current_set(self):
        if len(self.give_sets_with_least_covered_element()) == 0:
            return None
        return self.give_sets_with_least_covered_element()[self.give_branch_position()]

    def give_final_cover_sets(self):
        return list(self.current_cover_sets)  # + [self.give_current_set()]

    def add_tree_layer(
        self, surviving_elements, surviving_sets, sets_containing_least_covered_element
    ):
        self.location.append(0)
        self.surviving_elements_tree.append(surviving_elements)
        self.surviving_sets_tree.append(surviving_sets)
        self.sets_containing_least_covered__element_tree.append(
            sets_containing_least_covered_element
        )
        self.current_cover_sets.append(self.give_current_set())

    def is_on_first_layer(self):
        return len(self.location) <= 1


def algorithmX(cover, reqLst=[]):
    numberOfEle, numberOfSets = cover.shape
    initial_elements = np.arange(numberOfEle)
    initial_sets = np.arange(numberOfSets)
    [initial_elements, initial_sets] = removeReq(
        cover, initial_elements, initial_sets, reqLst
    )
    sets_containing_least_covered_element = give_sets(
        cover, initial_elements, initial_sets
    )

    if len(initial_elements) == 0:
        return []

    tree = AlgorithmXTree(
        initial_elements, initial_sets, sets_containing_least_covered_element
    )

    while 1:
        # if the minimum number of 1s is 0 the problem isn't solved and we must go back up the tree
        if sets_containing_least_covered_element.size == 0:

            # goes through the tree, if all branches have been looked at it goes back up the tree until it can find a new branch
            while 1:
                if tree.is_not_on_final_branch():
                    tree.increment_branch_position()
                    break
                if tree.is_on_first_layer():
                    return None  # returns None if unsolvable
                tree.go_up_a_layer()

            sets_containing_least_covered_element = give_sets(
                cover, tree.give_surviving_elements(), tree.give_surviving_sets()
            )

        else:  # if the minimum number of ones is not 0 continue onto the next level of Tree
            surviving_elements, surviving_sets = give_elements_and_sets_after_deletion(
                cover,
                tree.give_surviving_elements(),
                tree.give_surviving_sets(),
                tree.give_current_set(),
            )
            if len(surviving_elements) == 0:
                return tree.give_final_cover_sets()

            sets_containing_least_covered_element = give_sets(
                cover, surviving_elements, surviving_sets
            )
            tree.add_tree_layer(
                surviving_elements,
                surviving_sets,
                sets_containing_least_covered_element,
            )


def int2Board(lst):
    board = np.zeros((9, 9), dtype=int)
    for item in lst:
        t = int_to_base_9(item)
        board[t[0], t[1]] = t[2] + 1

    return board


def lst2Board(lst):
    board = np.zeros((9, 9), dtype=int)
    for item in lst:
        board[item[0], item[1]] = item[2] + 1

    return board


def board2Lst(board):
    nonzeros = np.nonzero(board)

    lst = []
    for i in range(len(nonzeros[0])):
        lst.append(
            (nonzeros[0][i], nonzeros[1][i], board[nonzeros[0][i], nonzeros[1][i]] - 1)
        )

    return lst


def SolveSudoku(board):
    cover = create_sudoku_cover()
    reqLst = board2Lst(board)
    solvedSquares = [int_to_base_9(idx) for idx in algorithmX(cover, reqLst)]
    return lst2Board(reqLst + solvedSquares)
