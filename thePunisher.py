import time
import Reversi
import HashMap
import random
import sys
from playerInterface import *


BOARDSIZE = 8
SEED = 13459
HASHSIZE = 100000
hashTable = HashMap.HashTable(HASHSIZE)
DEADLINE = round(time.time()*1000) + 1000*60*5

class thePunisher(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._name = "The Punisher"
        self._startFlag = 0
        self.deadline = 9999
        self._eval = [[35,-4,0,12,10,10,12,0,-4,35],
                       [-4,-6,1,1,1,1,1,1,-6,-4],
                       [0,0,1,1,1,1,1,1,0,0],
                       [12,1,1,4,3,3,4,1,1,12],
                       [10,1,1,3,2,2,3,1,1,10],
                       [10,1,1,3,2,2,3,1,1,10],
                       [12,1,1,4,3,3,4,1,1,12],
                       [0,0,1,1,1,1,1,1,0,0],
                       [-6,-8,1,1,1,1,1,1,-8,-6],
                       [35,-6,0,12,10,10,12,0,-6,35]]

    def getPlayerName(self):
        return self._name

    def getPlayerMove(self):
        #initialize the deadline
        if self._startFlag == 0:
            self._deadline = DEADLINE
            self._startFlag = 1

        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)


        #if there is not enough time -> random
        if (self._startFlag):
            if (self._deadline - time.time() < 1000):
                moves = self._board.legal_moves()
                (c, x, y) = moves[random.randint(0, len(moves)-1)]
                return (x, y)

        endTime = round(time.time()*1000.0) + 4000.0
        maxi = -2**31
        bestMove = [self._board._nextPlayer, -1, -1]
        depth = 3

        #Progressive deepening
        while(round(time.time()*1000.0) < endTime):
            result = self.search(self._board, depth, endTime)
            if (result[0] > maxi):
                bestMove = result[1]
            depth += 1
        print("DEPTH : ", depth)
        self._board.push(bestMove)
        print("I am playing ", bestMove)
        (c,x,y) = bestMove
        assert(c == self._mycolor)
        print("My current board :")
        print(self._board)

        return (x,y)

    def playOpponentMove(self, x, y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


    def search(self, b, maxDepth, endTime):

        maxi = -2**31
        bestMove = [b._nextPlayer, -1, -1]
        alpha = -2**31
        beta = 2**31

        moves = b.legal_moves()
        # self.quickSort(b, moves, 0, len(moves) - 1)

        for move in moves :
            if (time.time()*1000.0 > endTime):
                break;

            b.push(move)

            score = self.jouerMin(b, maxDepth - 1, alpha, beta)
            if (score > maxi):
                maxi = score
                bestMove = move

            b.pop()

        return (maxi, bestMove)


    def jouerMax(self, b, depth, alpha, beta):

        if (depth == 0):
            return self.heuristique(b._nextPlayer)
            # return self.computeEvaluation(b)

        maxi = -2**31
        for move in b.legal_moves() :
            b.push(move)
            maxi = max(maxi, self.jouerMin(b, depth - 1, alpha, beta))
            b.pop()

            alpha = max(alpha, maxi)
            if alpha >= beta:
                break  # beta cut-off

        return maxi


    def jouerMin(self, b, depth, alpha, beta):

        if (depth == 0):
            return self.heuristique(b._nextPlayer)
            # return self.computeEvaluation(b)

        mini = 2**31
        for move in b.legal_moves() :
            b.push(move)
            mini = min(mini, self.jouerMax(b, depth - 1, alpha, beta))
            b.pop()

            beta = min(beta, mini)
            if alpha >= beta:
                break  # alpha cut-off

        return mini


    def computeEvaluation(self, b):
        global hashTable
        get_result = hashTable.get(b)
        if (get_result is not None):
            return get_result
        else:
            eval = self.heuristique(b._nextPlayer)
            hashTable.add(b, eval)
            return eval


    # def heuristique(self, player=None):
    #     if player is None:
    #         player = self._board._nextPlayer
    #
    #     #############################
    #     ######## Cell Score #########
    #     #############################
    #     my_score = 0
    #     opp_score = 0
    #     for x in range(self._board._boardsize):
    #         for y in range(self._board._boardsize):
    #             if (self._board._board[x][y] == self._board._WHITE):
    #                 if (player is self._board._WHITE):
    #                     my_score += self._eval[x][y]
    #                 else:
    #                     opp_score += self._eval[x][y]
    #             elif (self._board._board[x][y] == self._board._BLACK):
    #                 if (player is self._board._BLACK):
    #                     my_score += self._eval[x][y]
    #                 else:
    #                     opp_score += self._eval[x][y]
    #
    #     c = my_score - opp_score
    #
    #     #############################
    #     ######## Coin Parity ########
    #     #############################
    #     if player is self._board._WHITE:
    #         cp = 100 * (self._board._nbWHITE - self._board._nbBLACK) / (self._board._nbWHITE + self._board._nbBLACK)
    #     else:
    #         cp = 100 *(self._board._nbBLACK - self._board._nbWHITE) / (self._board._nbBLACK + self._board._nbWHITE)
    #
    #     #############################
    #     ######## Mobility ###########
    #     #############################
    #     moves = self._board.legal_moves()
    #     my_mobility = len(moves)
    #     opp_mobility = 0
    #
    #     for move in moves:
    #         self._board.push(move)
    #         opp_mobility += len(self._board.legal_moves())
    #         self._board.pop()
    #     opp_mobility = opp_mobility / my_mobility
    #
    #     if my_mobility + opp_mobility != 0:
    #         m = 100 * (my_mobility - opp_mobility) / (my_mobility + opp_mobility)
    #     else:
    #         m = 0
    #
    #
    #     if (self._board.is_game_over()):
    #         end_game = 100000
    #     else:
    #         end_game = 0
    #
    #     return c + cp +  2 * m


    def heuristique(self, player=None):
        if player is None:
            player = self._board._nextPlayer

        ############################
        ####### Coin Parity ########
        ############################
        if player is self._board._WHITE:
            cp =  (self._board._nbWHITE - self._board._nbBLACK) / (self._board._nbWHITE + self._board._nbBLACK)
        else:
            cp =  (self._board._nbBLACK - self._board._nbWHITE) / (self._board._nbBLACK + self._board._nbWHITE)



        ############################
        #### Corner occupancy ######
        ############################
        my_corners = 0
        opp_corners = 0
        boardsize = self._board._boardsize

        if player is self._board._WHITE:
            if self._board._board[0][0] == self._board._WHITE: my_corners += 1
            elif self._board._board[0][0] == self._board._BLACK: opp_corners += 1

            if self._board._board[0][boardsize - 1] == self._board._WHITE: my_corners += 1
            elif self._board._board[0][boardsize - 1] == self._board._BLACK: opp_corners += 1

            if self._board._board[boardsize - 1][0] == self._board._WHITE: my_corners += 1
            elif self._board._board[boardsize - 1][0] == self._board._BLACK: opp_corners += 1

            if self._board._board[boardsize - 1][boardsize - 1] == self._board._WHITE: my_corners += 1
            elif self._board._board[boardsize - 1][boardsize - 1] == self._board._BLACK: opp_corners += 1

        else:
            if self._board._board[0][0] == self._board._BLACK: my_corners += 1
            elif self._board._board[0][0] == self._board._WHITE: opp_corners += 1

            if self._board._board[0][boardsize - 1] == self._board._BLACK: my_corners += 1
            elif self._board._board[0][boardsize - 1] == self._board._WHITE: opp_corners += 1

            if self._board._board[boardsize - 1][0] == self._board._BLACK: my_corners += 1
            elif self._board._board[boardsize - 1][0] == self._board._WHITE: opp_corners += 1

            if self._board._board[boardsize - 1][boardsize - 1] == self._board._BLACK: my_corners += 1
            elif self._board._board[boardsize - 1][boardsize - 1] == self._board._WHITE: opp_corners += 1


        co = 25 * (my_corners - opp_corners)


        ############################
        ##### Corner closeness #####
        ############################
        my_close_corners = 0
        opp_close_corners = 0

        if player is self._board._WHITE:
            if (self._board._board[0][0] == self._board._EMPTY):
                if self._board._board[0][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[0][1] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][0] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][0] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][1] == self._board._BLACK: opp_close_corners += 1

            if (self._board._board[0][boardsize - 1] == self._board._EMPTY):
                if self._board._board[0][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[0][boardsize - 2] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][boardsize - 2] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][boardsize - 1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][boardsize - 1] == self._board._BLACK: opp_close_corners += 1

            if (self._board._board[boardsize - 1][0] == self._board._EMPTY):
                if self._board._board[boardsize - 2][0] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][0] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 2][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][1] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 1][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 1][1] == self._board._BLACK: opp_close_corners += 1

            if (self._board._board[boardsize - 1][boardsize - 1] == self._board._EMPTY):
                if self._board._board[boardsize - 1][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 1][boardsize - 2] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 1] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 2] == self._board._BLACK: opp_close_corners += 1

        else:
            if (self._board._board[0][0] == self._board._EMPTY):
                if self._board._board[0][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[0][1] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][0] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][0] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][1] == self._board._WHITE: opp_close_corners += 1

            if (self._board._board[0][boardsize - 1] == self._board._EMPTY):
                if self._board._board[0][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[0][boardsize - 2] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][boardsize - 2] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][boardsize - 1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][boardsize - 1] == self._board._WHITE: opp_close_corners += 1

            if (self._board._board[boardsize - 1][0] == self._board._EMPTY):
                if self._board._board[boardsize - 2][0] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][0] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 2][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][1] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 1][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 1][1] == self._board._WHITE: opp_close_corners += 1

            if (self._board._board[boardsize - 1][boardsize - 1] == self._board._EMPTY):
                if self._board._board[boardsize - 1][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 1][boardsize - 2] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 1] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 2] == self._board._WHITE: opp_close_corners += 1

        cc = -12.5 * (my_close_corners - opp_close_corners);

        ############################
        ######### Mobility #########
        ############################
        moves = self._board.legal_moves()
        my_mobility = len(moves)
        opp_mobility = 0

        for move in moves:
            self._board.push(move)
            opp_mobility += len(self._board.legal_moves())
            self._board.pop()
        opp_mobility = opp_mobility / my_mobility

        if my_mobility + opp_mobility != 0:
            m = (my_mobility - opp_mobility) / (my_mobility + opp_mobility)
        else:
            m = 0

        ############################
        ######### End game #########
        ############################
        if (self._board.is_game_over()):
            end_game = 100000
        else:
            end_game = 0


        return 100 * cp + (800 * co) + (300 * cc) + end_game + (200 * m)

    def heuristique(self, player=None):
        if player is None:
            player = self._nextPlayer
        if player is self._board._WHITE:
            return self._board._nbWHITE - self._board._nbBLACK
        return self._board._nbBLACK - self._board._nbWHITE


    def quickSort(self, b, moves, low, high):
        if low < high:
            pi = self.partition(b, moves, low, high)
            self.quickSort(b, moves, low, pi-1)
            self.quickSort(b, moves, pi+1, high)


    def partition(self, b, moves, low, high):
        i = low - 1
        b.push(moves[high])
        pivot = self.computeEvaluation(b)
        b.pop()

        for j in range(low , high):
            b.push(moves[j])
            evalJ = self.computeEvaluation(b)
            b.pop()

            if  evalJ <= pivot:
                i = i+1
                moves[i], moves[j] = moves[j], moves[i]

        moves[i+1], moves[high] = moves[high], moves[i+1]
        return i + 1


#######################################
############# UTIL FUNCTIONS ##########
#######################################

#
# def quickSort(b, moves, low, high):
#     if low < high:
#         pi = partition(b, moves, low, high)
#         quickSort(b, moves, low, pi-1)
#         quickSort(b, moves, pi+1, high)
#
#
# def partition(b, moves, low, high):
#     i = low - 1
#     b.push(moves[high])
#     pivot = self.computeEvaluation(b)
#     b.pop()
#
#     for j in range(low , high):
#         b.push(moves[j])
#         evalJ = self.computeEvaluation(b)
#         b.pop()
#
#         if  evalJ <= pivot:
#             i = i+1
#             moves[i], moves[j] = moves[j], moves[i]
#
#     moves[i+1], moves[high] = moves[high], moves[i+1]
#     return i + 1



###############################
######### HASH MAP ############
###############################


# a table with random 64 bits numbers
# table[sizeBoard][sizeBoard][2]
random.seed(SEED)
table = [[[random.getrandbits(64), random.getrandbits(64)] for x in range(BOARDSIZE)] for y in range(BOARDSIZE)]

def generateZobristKey(b):
    global table
    hash = 0
    board = b._board

    for x in range(b._boardsize):
        for y in range(b._boardsize):
            if board[x][y] != b._EMPTY:
                piece = board[x][y]
                hash ^= table[x][y][piece - 1]
    return hash



class HashTable:
        def __init__(self, size):
                self.size = size
                self.map = [None] * self.size

        def _get_hash(self, zobristKey):
                return zobristKey % self.size

        def add(self, board, evaluation): # we can add more values
                key = generateZobristKey(board)
                key_hash = self._get_hash(key)
                key_value = [key, evaluation]

                if self.map[key_hash] is None:
                        self.map[key_hash] = list([key_value])
                        return True
                else:
                        for pair in self.map[key_hash]:
                                if pair[0] == key:
                                        pair[1] = evaluation
                                        return True
                        self.map[key_hash].append(key_value)
                        return True

        def get(self, board):
                key = generateZobristKey(board)
                key_hash = self._get_hash(key)
                if self.map[key_hash] is not None:
                        for pair in self.map[key_hash]:
                                if pair[0] == key:
                                        return pair[1]
                return None

        def delete(self, board):
                key = generateZobristKey(board)
                key_hash = self._get_hash(key)

                if self.map[key_hash] is None:
                        return False
                for i in range (0, len(self.map[key_hash])):
                        if self.map[key_hash][i][0] == key:
                                self.map[key_hash].pop(i)
                                return True
                return False

        def keys(self):
                arr = []
                for i in range(0, len(self.map)):
                        if self.map[i]:
                                arr.append(self.map[i][0])
                return arr

        def display(self):
                print('---HASH TABLE----')
                for item in self.map:
                        if item is not None:
                                print(str(item))
