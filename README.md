# Introduction
This repository animate the solution of the 8 queens puzzle (and the general case of N queens puzzle) using a backtracking algorithm.

# Eight Queens Puzzle
The 8 queens puzzle is concerned with placing 8 queens in an <img src="https://latex.codecogs.com/svg.image?8\times8" title="https://latex.codecogs.com/svg.image?8\times8" /> chess board such that no queen threatens any other queen. Please read more on the eight queens puzzle [here](https://en.wikipedia.org/wiki/Eight_queens_puzzle). In this repo we present a solution to the general N queens puzzle in <img src="https://latex.codecogs.com/svg.image?N\times&space;N" title="https://latex.codecogs.com/svg.image?N\times N" /> chess board.

# Backtracking
Backtracking is a general problem solving technique that builds a solution incrementally and abandons "backtracks" a candidate move if it will lead to invalid solution. Please read more on backtracking [here](https://en.wikipedia.org/wiki/Backtracking). In the case of the eight aueens puzzle, assume we placed <img src="https://latex.codecogs.com/svg.image?k-1" title="https://latex.codecogs.com/svg.image?k-1" /> queens in the first <img src="https://latex.codecogs.com/svg.image?k-1" title="https://latex.codecogs.com/svg.image?k-1" /> rows. The algorithm places a queen in the <img src="https://latex.codecogs.com/svg.image?k^{th}" title="https://latex.codecogs.com/svg.image?k^{th}" /> row as long as it does not threaten a previously placed queen in any of the previous rows. If that is not possible, the algorithm removes the queen in the <img src="https://latex.codecogs.com/svg.image?(k-1)^{th}" title="https://latex.codecogs.com/svg.image?(k-1)^{th}" /> row and try to find a new position for it. If it succeeds, it proceeds forward. Otherwise, it goes backward again to the <img src="https://latex.codecogs.com/svg.image?(k-2)^{th}" title="https://latex.codecogs.com/svg.image?(k-2)^{th}" /> row and so on.

# Animation
In the animation, the forward move is hightlighted in yellow, the backward move is highlighted in red, and a solid red line is drawn to connect the two queens that threaten each other. Watch the animation:


https://user-images.githubusercontent.com/46744732/184110003-bef2553d-aa58-4ab5-853f-a275aa14b266.mp4

