#!/usr/bin/env python
"""
This module animates the steps of the backtracking algorithm applied to the N Queen Puzzle).
"""

__author__  = "Ahmed Hassan"
__license__ = "MIT License"
__version__ = "1.0"
__date__    = "11-08-2022"
__email__   = "ahmedhassan@aims.ac.za"
__status__  = "Prototype"


import pygame
import sys


class QueenPuzzle:
    """
    A class for solving the n queen puzzle using the backtracking technique.
    The class animates the steps of the backtracking technique.
    """

    def __init__(self, nQueens, width=600, height=600, speed=2):
        """
        Initialize the class and pygame
        :param nQueens: number of queens
        :param width: width of display window. Default is 600.
        :param height: height of display window. Default is 600.
        :param speed: animation speed
        """

        pygame.init()  # Make pygame ready.
        self.nQueens = nQueens  
        self.width = width  
        self.height = height  
        # Screen.
        self.screen = pygame.display.set_mode((width, height))
        # Caption.
        pygame.display.set_caption("Backtracking: Queen Puzzle")
        # Size of each square in the chessboard.
        self.square_size = width // self.nQueens
        # Chessboard as a two-dimensional array.
        # Note that for backtracking, the chessboard can be represented as
        # a one-dimensional array in which a[j] refers to the column in the jth row.
        # However, we chose to use a two-dimensional array in order to draw each square
        # in the chessboard onto the screen.
        self.chessboard = []
        # The queen that is to be placed for this iteration.
        self.current_queen = Queen(self.square_size, self.square_size)
        # All queens that have been placed so far.
        self.queens_group = pygame.sprite.Group()
        # queens_list is the same as queens_group. However, we use a list since
        # pygame.sprite.Group does not support removing by index (last element for example).
        # We use gueens_group since it is easy to draw all queens at once and we
        # use queens_list to remove the last element in case of a back step.
        # You could use a list without the group and draws all queens by using a loop.
        self.queens_list = []
        # The speed of animation (rate of frames per second)
        self.speed = speed


    def _draw_chessboard_and_queens(self):
        """
        Draw the chessboard and the queens placed so far.
        :return:
        """
        # Square color.
        WHITE = pygame.Color('white')
        BLACK = pygame.Color('darkgray')
        # Chessboard.
        self.chessboard = []
        color = WHITE
        for r in range(self.nQueens):
            # If the number of queens is even, we need to alternate the colors
            # of the first square in each row
            if nQueens % 2 == 0:
                color = WHITE if color == BLACK else BLACK
            y = r * self.square_size
            row = []
            for c in range(self.nQueens):
                x = c * self.square_size
                rect = pygame.Rect(x, y, self.square_size, self.square_size)
                row.append(rect)
                self.screen.fill(color, rect)
                color = WHITE if color == BLACK else BLACK
            self.chessboard.append(row)

        # Draw all queens at once.
        self.queens_group.draw(self.screen)


    def _check_events(self):
        """
        Check for events.
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Also close the game if user press "q".
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()


    def _update_queen_position(self, row, col):
        """
        Update the current queen position to be in row and col.
        :param row:
        :param col:
        :return:
        """
        square = self.chessboard[row][col]
        pos = (square.centerx, square.centery)
        self.current_queen.update(pos, row, col)
        self.current_queen.blitme(self.screen)


    def _place_queen(self, row, col):
        """
        Place the current queen in the specified position (row, col) and
        create a new queen to be placed in the next row.
        :param row:
        :param col:
        :return:
        """
        square = self.chessboard[row][col]
        pos = (square.centerx, square.centery)
        self.current_queen.update(pos, row, col)
        self.queens_group.add(self.current_queen)
        self.queens_list.append(self.current_queen)
        self.current_queen = Queen(self.square_size, self.square_size)
        if row + 1 < len(self.chessboard[0]):
            square = self.chessboard[row + 1][0]
        pos = (square.centerx, square.centery)
        self.current_queen.update(pos, row, col)
        self.current_queen.blitme(self.screen)


    def _remove_queen(self):
        """
        A back step! Remove the last placed queen since a new queen cannot be placed
        in the next row.
        :return:
        """
        queen = self.queens_list.pop()
        self.queens_group.remove(queen)

    def _highlight_conflict(self, row1, col1, row2, col2):
        """
        Highlight a conflict. A conflict occurs if:
            1. Two queens share the same row or the same column.
            2. Two queens share the same diagonal.
        :param row1:
        :param col1:
        :param row2:
        :param col2:
        :return:
        """
        rect1 = self.chessboard[row1][col1]
        rect2 = self.chessboard[row2][col2]
        start = (rect1.centerx, rect1.centery)
        end = (rect2.centerx, rect2.centery)
        pygame.draw.line(self.screen, pygame.Color('red'), start, end, 10)


    def _highlight_current_row(self, row, backtrack=False):
        """
        Highlight the "current row".
        The current row means the following:
            1. In a forward step, the current row is the row in which the current queen is attempted
            to be placed. In this case, it is highlighted in yellow.
            2. In a backward step, the current row is the row from which a queen have to be removed.
            In this case, it is highlighted in red.
        :param row:
        :param backtrack:
        :return:
        """
        # If the row fall outside the board ignore it
        if row < 0 or row >= self.nQueens:
            return
        # Highlight color. Either yellow (forward) or red (backward).
        color = pygame.Color('red') if backtrack else pygame.Color('yellow')
        rect = self.chessboard[row][0]
        surface_rect = pygame.Rect(0, 0, self.width, self.square_size)
        surface_rect.left = rect.left
        surface_rect.top = rect.top
        surface = pygame.Surface((self.width, self.square_size))
        surface.set_alpha(125)
        surface.fill(color)
        # Draw the surface on the screen
        self.screen.blit(surface, surface_rect)


    def _find_position(self, row, start, clock):
        """
        In row "row" and starting from column "start" find a position for the queen.
        :param row:
        :param start:
        :param clock:
        :return:
        """
        # Check all available columns
        for col in range(start, self.nQueens):
            conflicting_queen = None
            # Check all placed queens for conflict
            for queen in self.queens_list:
                # Check for events, e.g. if the user wants to quit
                self._check_events()
                qrow = queen.row
                qcol = queen.col
                same_col = qcol == col  # same column
                bottom_left_diag = qcol == col - (row - qrow)  # bottom left diagonal
                bottom_right_diag = qcol == col + (row - qrow)  # bottom right diagonal
                if same_col or bottom_left_diag or bottom_right_diag:
                    conflicting_queen = queen
                    break
            # Animation the search for a position
            self._draw_chessboard_and_queens()
            self._update_queen_position(row, col)
            if conflicting_queen:
                self._highlight_conflict(row, col, conflicting_queen.row, conflicting_queen.col)
                pygame.display.flip()
                clock.tick(1.5*self.speed)
            else:
                pygame.display.flip()
                clock.tick(1.5*self.speed)
                return col
        return -1

    def _listen_to_user(self):
        """
        Pause until the user quit.
        :return:
        """
        # Draw whatever on the screen
        pygame.display.flip()
        while True:
            self._check_events()

    def _fail_to_solve(self):
        self._draw_chessboard_and_queens()
        surface = pygame.Surface((self.width, self.height))
        surface.set_alpha(125)
        surface.fill(pygame.Color('red'))
        self._listen_to_user()

    def solve(self):
        """
        Use the backtracking technique to solve the puzzle.
        :return:
        """
        # Clock to control the animation speed
        clock = pygame.time.Clock()
        self._draw_chessboard_and_queens()
        # Update the screen
        pygame.display.flip()
        current_row = 0
        start = 0 # the column from which we start
        while (current_row >= 0 and current_row < self.nQueens):
            # Find a position for the current queen
            col = self._find_position(current_row, start, clock)
            # Check for events, e.g. if user wants to quit the animation
            self._check_events()
            # If a position is found
            if col != -1:
                backtrack_flag = False # Moving forward
                self._place_queen(current_row, col) # Place the queen
                self._draw_chessboard_and_queens() # Draw stuff
                self._highlight_current_row(current_row + 1, backtrack_flag) # Highlight with yellow
                current_row += 1 # Move to next row
                start = 0 # Start from the first column
            else:
                backtrack_flag = True
                current_row -= 1
                # If the puzzle cannot be solved, current_row becomes negative
                if current_row >= 0:
                    self._draw_chessboard_and_queens()
                    self._highlight_current_row(current_row, backtrack_flag)
                    start = self.queens_list[-1].col + 1 # Start from next column
                    self._remove_queen()

            # If all queens have been placed, listen to the user if he wants to quit
            if current_row == self.nQueens:
                self._listen_to_user()

            # If all cannot be placed, draw the board and listen to the user
            if current_row < 0:
                self._fail_to_solve()

            pygame.display.flip()
            clock.tick(self.speed)


class Queen(pygame.sprite.Sprite):
    """
    A class for representing a queen in the chess board.
    """

    def __init__(self, width=0, height=0):
        super().__init__();
        self.image = pygame.image.load('Images/queen.png')
        # Adjust the queen dimensions to be the same as the square dimensions
        if width != 0 and height != 0:
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.centerx = 0
        self.centery = 0
        self.row = 0 # Needed for checking for conflicts
        self.col = 0 # Needed for checking for conflicts

    def update(self, pos, row, col):
        """
        Update the queen position.
        :param pos:
        :param row:
        :param col:
        :return:
        """
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.row = row
        self.col = col

    def blitme(self, screen):
        """
        Draw the queen on the screen at the specified position
        :param screen:
        :return:
        """
        screen.blit(self.image, self.rect)


if __name__ == '__main__':
    nQueens = 8 # Number of queens
    speed = 1.5 # Animation speed
    screen_size = 800 # Screen size
    puzzle = QueenPuzzle(nQueens, screen_size, screen_size, speed)
    puzzle.solve()
