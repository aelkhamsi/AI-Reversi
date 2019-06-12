# AI-Reversi

This projects implements the game Reversi (Reversi.py) and several AIs that can play against each other.

4 AIs are available:
  
    1. random : this AI plays random moves in each round
    2. minimax : this AI use the minimax algorithm to play its moves
    3. alphabeta : this AI use the algorithm alphabeta to play its move
    4. iterativeDeepening : this AI use the alphabeta algorithm with the technique of iterative deepening for time management
    

to play some games : 

$ python3 minimax.py : 2 minimax AIs play against each other with a search depth of 4 and infinite time
$ python3 alphabeta.py : 2 alphabeta AIs play against each other with a search depth of 4 and infinite time
$ python3 iterativeDeepening.py : 2 iterativeDeepening AIs play against each other with a search depth of 4 and a maximum total time of 20 seconds
$ python3 localGame.py : A random AI play against an itertaiveDeepening AI with a maximum total time of 5 min per player
