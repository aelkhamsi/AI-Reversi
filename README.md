# AI-Reversi

The game of Reversi is a strategy game for two players, played on an 8x8 board. In this project, we've tried to explore some of the search algorithms to implement an AI that can play Reversi. In each round, we will look ahead and evaluate different combinations of moves in order to find the best move possible. The algorithms implemented in this project are minimax algorithms and αβ (alphabeta) algorithm for search and iterative deepening for time managment.

## Technologies used
* Python

## Commands

4 AIs are available:

    1. random : this AI plays random moves in each round
    2. minimax : this AI use the minimax algorithm to play its moves
    3. alphabeta : this AI use the algorithm alphabeta to play its move
    4. iterativeDeepening : this AI use the alphabeta algorithm with the technique of iterative deepening for time management
    

to make AIs play against each other, several commands are available depending on the algorithm used by the AIs.

* 2 minimax AIs play against each other with a search depth of 4 and infinite time 
```bash
python3 minimax.py
```
* 2 alphabeta AIs play against each other with a search depth of 4 and infinite time 
```bash
python3 alphabeta.py
```
* 2 iterativeDeepening AIs play against each other with a search depth of 4 and a maximum total time of 20 seconds
```bash
python3 iterativeDeepening.py
```
* A random AI play against an itertaiveDeepening AI with a maximum total time of 5 min per player
```bash
python3 localGame.py
```

