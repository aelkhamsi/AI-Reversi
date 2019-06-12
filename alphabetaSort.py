import time
import Reversi
import HashMap
from random import randint, choice
import sys

HASHSIZE = 500000
hashTable = HashMap.HashTable(HASHSIZE)
depth = 4

counter = 0
movesSample = []
movesSampleSorted = []


def deroulementAlphabeta(b, maxDepth):
    # print("------------------------")
    global counter
    global flag
    global movesSample
    global movesSampleSorted

    counter += 1
    if b.is_game_over():
        return

    maxi = -2**31
    maxMove = [b._nextPlayer, -1, -1]
    alpha = -2**31
    beta = 2**31

    moves = b.legal_moves()
    if counter == 30:
        movesSample = moves
    quickSort(b, moves, 0, len(moves) - 1)
    if counter == 30:
        movesSampleSorted = moves

    for move in reversed(moves):
        b.push(move)

        score = jouerMin(b, maxDepth - 1, alpha, beta)
        if (score > maxi):
            maxi = score
            maxMove = move

        b.pop()

    b.push(maxMove)
    # print(b)
    deroulementAlphabeta(b, maxDepth)


def jouerMax(b, depth, alpha, beta):

    if (depth == 0):
        return b.heuristique(b._nextPlayer)
        # return computeEvaluation(b)  #more slow that calculating the heuristic !?

    maxi = -2**31
    for move in b.legal_moves() :
        b.push(move)
        maxi = max(maxi, jouerMin(b, depth - 1, alpha, beta))
        b.pop()

        alpha = max(alpha, maxi)
        if alpha >= beta:
            break  # beta cut-off

    return maxi


def jouerMin(b, depth, alpha, beta):

    if (depth == 0):
        return b.heuristique(b._nextPlayer)
        # return computeEvaluation(b)  #more slow that calculating the heuristic !?

    mini = 2**31
    for move in b.legal_moves() :
        b.push(move)
        mini = min(mini, jouerMax(b, depth - 1, alpha, beta))
        b.pop()

        beta = min(beta, mini)
        if alpha >= beta:
            break  # alpha cut-off

    return mini




#######################################
############# UTIL FUNCTIONS ##########
#######################################


def computeEvaluation(b):
    global hashTable
    get_result = hashTable.get(b)
    if (get_result is not None):
        return get_result
    else:
        eval = b.heuristique(b._nextPlayer)
        hashTable.add(b, eval)
        return eval


def quickSort(b, moves, low, high):
    if low < high:
        pi = partition(b, moves, low, high)
        quickSort(b, moves, low, pi-1)
        quickSort(b, moves, pi+1, high)


def partition(b, moves, low, high):
    i = low - 1
    b.push(moves[high])
    pivot = computeEvaluation(b)
    b.pop()

    for j in range(low , high):
        b.push(moves[j])
        evalJ = computeEvaluation(b)
        b.pop()

        if  evalJ <= pivot:
            i = i+1
            moves[i], moves[j] = moves[j], moves[i]

    moves[i+1], moves[high] = moves[high], moves[i+1]
    return i + 1


# def partition(arr,low,high):
#     i = ( low-1 )
#     pivot = arr[high]
#
#     for j in range(low , high):
#         if   arr[j] <= pivot:
#             i = i+1
#             arr[i],arr[j] = arr[j],arr[i]
#
#     arr[i+1],arr[high] = arr[high],arr[i+1]
#     return ( i+1 )
#
# def quickSort(arr,low,high):
#     if low < high:
#         pi = partition(arr,low,high)
#         quickSort(arr, low, pi-1)
#         quickSort(arr, pi+1, high)


#######################################
############# TEST ####################
#######################################


board = Reversi.Board()

ts = time.time();
deroulementAlphabeta(board, depth)
ts = time.time() - ts;

print(ts)
# print(movesSample)
# print(movesSampleSorted)
