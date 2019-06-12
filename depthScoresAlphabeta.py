import time
import Reversi
from random import randint, choice
import sys


depth = 4
tours = 0

def deroulementAlphabeta(b, maxDepth):
    global tours
    tours += 1
    if b.is_game_over():
        return

    maxi = -2**31
    maxMove = [b._nextPlayer, -1, -1]
    alpha = -2**31
    beta = 2**31

    for move in b.legal_moves() :
        b.push(move)

        score = jouerMin(b, maxDepth - 1, alpha, beta)
        if (score > maxi):
            maxi = score
            maxMove = move

        b.pop()

    b.push(maxMove)
    deroulementAlphabeta(b, maxDepth)


def jouerMax(b, depth, alpha, beta):

    if (depth == 0):
        return b.heuristique(b._nextPlayer)

    maxi = -2**31
    for move in b.legal_moves() :
        b.push(move)
        maxi = max(maxi, jouerMin(b, depth - 1, alpha, beta))
        b.pop()

        alpha = max(alpha, maxi)
        if alpha >= beta:
            return beta  # beta cut-off

    return maxi


def jouerMin(b, depth, alpha, beta):

    if (depth == 0):
        return b.heuristique(b._nextPlayer)

    mini = 2**31
    for move in b.legal_moves() :
        b.push(move)
        mini = min(mini, jouerMax(b, depth - 1, alpha, beta))
        b.pop()

        beta = min(beta, mini)
        if alpha >= beta:
            return alpha  # alpha cut-off

    return mini



board = Reversi.Board()

for maxDepth in range(1, 5):
    board = Reversi.Board()

    ts = time.time()
    deroulementAlphabeta(board, maxDepth)
    ts = time.time() - ts

    print("Time for maxDepth = " + str(maxDepth) + " : ", end = '')
    print(ts, end = '  nb_tours : ')
    print(tours / 2)
