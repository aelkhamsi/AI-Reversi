import time
import Reversi
from random import randint, choice
import sys



def deroulementMinimax(b, maxDepth):

    if b.is_game_over():
        return

    maxi = -2**31
    maxMove = [b._nextPlayer, -1, -1]

    for move in b.legal_moves() :
        b.push(move)

        score = jouerMin(b, maxDepth - 1)
        if (score > maxi):
            maxi = score
            maxMove = move

        b.pop()

    b.push(maxMove)

    deroulementMinimax(b, maxDepth)


def jouerMax(b, depth):
    if (depth == 0):
        return b.heuristique(b._nextPlayer)

    maxi = -2**31
    for move in b.legal_moves() :
        b.push(move)
        maxi = max(maxi, jouerMin(b, depth - 1))
        b.pop()

    return maxi


def jouerMin(b, depth):
    if (depth == 0):
        return b.heuristique(b._nextPlayer)

    mini = 2**31
    for move in b.legal_moves() :
        b.push(move)
        mini = min(mini, jouerMax(b, depth - 1))
        b.pop()

    return mini



for maxDepth in range(1, 5):
    board = Reversi.Board()

    ts = time.time()
    deroulementMinimax(board, maxDepth)
    ts = time.time() - ts

    print("Time for maxDepth = " + str(maxDepth) + " : ", end = '')
    print(ts)
