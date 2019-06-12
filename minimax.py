import time
import Reversi
from random import randint, choice
import sys

depth = 4


def deroulementMinimax(b, maxDepth):
    print("------------------------")

    if b.is_game_over():
        return

    maxi = -2**31
    maxMove = [b._nextPlayer, -1, -1]

    for move in b.legal_moves() :
        b.push(move)

        score = jouerMin(b, depth - 1)
        if (score > maxi):
            maxi = score
            maxMove = move

        b.pop()

    b.push(maxMove)

    print(b)
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



board = Reversi.Board()
deroulementMinimax(board, depth )
