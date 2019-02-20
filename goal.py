"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this BlobGoal to have the given target colour.
        """
        Goal.__init__(self, target_colour)

    def score(self, board: Block) -> int:
        """Return the current score based on the largest blob of the target
        colour for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        # Get a flattened representation of the board
        flat_board = board.flatten()

        # Create a representation of the board to keep track of visited blocks
        size = len(flat_board[0])
        visited = []
        for _ in range(size):
            visited.append([-1] * size)

        # Go through each cell, keeping track of the largest blob size
        max_blob_size = 0
        for i in range(size):
            for j in range(size):
                blob_size = self._undiscovered_blob_size((i, j),
                                                         flat_board, visited)
                
                if blob_size > max_blob_size:
                    max_blob_size = blob_size

        return max_blob_size

    def description(self) -> str:
        """Return a description of this goal.
        """
        return "Create the largest blob of this colour"

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # If the given position is out of bounds, or the cell at the given
        # position has already been visited, return 0
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= len(board[0]) or \
        pos[1] >= len(board[0]) or visited[pos[0]][pos[1]] == 1 or \
        visited[pos[0]][pos[1]] == 0:
            return 0

        # If the position is valid and the cell has not been visited yet
        else:
            # Return 0 and mark the cell if the cell is not the target colour
            if self.colour != board[pos[0]][pos[1]]:
                visited[pos[0]][pos[1]] = 0
                return 0

            # If the cell is the right colour
            else:
                # Mark the board
                visited[pos[0]][pos[1]] = 1

                # The size of the blob is equal to the size of the blobs to the
                # north, south, east, and west, plus 1
                north_size = self._undiscovered_blob_size((pos[0] - 1, pos[1]),
                                                          board, visited)
                east_size = self._undiscovered_blob_size((pos[0], pos[1] + 1),
                                                         board, visited)
                west_size = self._undiscovered_blob_size((pos[0], pos[1] - 1),
                                                         board, visited)
                south_size = self._undiscovered_blob_size((pos[0] + 1, pos[1]),
                                                          board, visited)

                return north_size + east_size + west_size + south_size + 1


class PerimeterGoal(Goal):
    """A goal to put the most possible units of this goal's target colour
    on the outer perimter of the Block.
    """

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this PerimeterGoal to have the given target colour.
        """
        Goal.__init__(self, target_colour)

    def score(self, board: Block) -> int:
        """Return the current score based on the number of target blocks
        surrounding the perimeter of the given board.

        The score is always greater than or equal to 0.
        """
        flat_board = board.flatten()
        board_size = len(flat_board[0])
        
        # Count the perimeter blocks of the target colour by looping through
        # each side simultaneously. Corner blocks are worth double points, so
        # are counted twice.
        score_count = 0
        for i in range(board_size):
            if self.colour == flat_board[i][0]:
                score_count += 1
            if self.colour == flat_board[i][board_size - 1]:
                score_count += 1
            if self.colour == flat_board[0][i]:
                score_count += 1
            if self.colour == flat_board[board_size - 1][i]:
                score_count += 1

        return score_count

    def description(self) -> str:
        """Return a description of this goal.
        """
        return "Surround the perimeter with this colour"

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
