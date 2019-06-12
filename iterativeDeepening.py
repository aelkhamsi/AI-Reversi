import time
import Reversi
import HashMap
from random import randint, choice
import sys

HASHSIZE = 1000000
hashTable = HashMap.HashTable(HASHSIZE)
depth = 4



def iterativeDeepening(b):
    endTime = round(time.time()*1000.0) + 250.0  # 0.25 seconde
    print('--------------------------------')
    depth = 1

    maxi = -2**31
    bestMove = [b._nextPlayer, -1, -1]

    if b.is_game_over():
        print(time.time() - ts)
        return

    #Progressive deepening
    while(round(time.time()*1000.0) < endTime):
        result = search(b, depth);
        if (result[0] > maxi):
            bestMove = result[1]
        depth += 1

    b.push(bestMove)
    print(depth)
    print(b)
    iterativeDeepening(b);



def search(b, maxDepth):

    maxi = -2**31
    bestMove = [b._nextPlayer, -1, -1]
    alpha = -2**31
    beta = 2**31

    moves = b.legal_moves()
    quickSort(b, moves, 0, len(moves) - 1)

    for move in moves :
        b.push(move)

        score = jouerMin(b, maxDepth - 1, alpha, beta)
        if (score > maxi):
            maxi = score
            bestMove = move

        b.pop()

    return (maxi, bestMove)


def jouerMax(b, depth, alpha, beta):

    if (depth == 0):
        # return b.heuristique(b._nextPlayer)
        return computeEvaluation(b)

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
        # return b.heuristique(b._nextPlayer)
        return computeEvaluation(b)

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




#######################################
############# TEST ####################
#######################################


board = Reversi.Board()
ts = time.time()
iterativeDeepening(board)
ts = time.time() - ts

print(ts)
