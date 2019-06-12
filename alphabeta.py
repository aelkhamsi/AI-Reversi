import time
import Reversi
from random import randint, choice
import sys


depth = 4

def deroulementAlphabeta(b, maxDepth):
    global depth
    print("------------------------")

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
    print(b)
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
            break  # beta cut-off

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
            break  # alpha cut-off

    return mini



board = Reversi.Board()

ts = time.time()
deroulementAlphabeta(board, depth)
ts = time.time() - ts
print(ts)
