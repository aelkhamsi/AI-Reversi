import Reversi
import random

BOARDSIZE = 8
SEED = 13459
HASHSIZE = 100000

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



# board = Reversi.Board()
# hashMap = HashMap(HASHSIZE)
#
# if hashMap.get(board) is None:
#     hashMap.add(board, 1)
#     hashMap.add(board, 2)
#
# hashMap.display()
# hashMap.delete(board)
