"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Game class, which is the main class for the
Blocky game.

At the bottom of the file, there are some function that you
can call to try playing the game in several different configurations.
"""
import random
from typing import List
from block import Block, random_init
from goal import BlobGoal, PerimeterGoal
from player import Player, HumanPlayer, RandomPlayer, SmartPlayer
from renderer import Renderer, COLOUR_LIST, colour_name, BOARD_WIDTH


class Game:
    """A game of Blocky.

    === Public Attributes ===
    board:
        The Blocky board on which this game will be played.
    renderer:
        The object that is capable of drawing our Blocky board on the screen,
        and tracking user interactions with the Blocky board.
    players:
        The entities that are playing this game.

    === Representation Invariants ===
    - len(players) >= 1
    """
    board: Block
    renderer: Renderer
    players: List[Player]

    def __init__(self, max_depth: int,
                 num_human: int,
                 random_players: int,
                 smart_players: List[int]) -> None:
        """Initialize this game, as described in the Assignment 2 handout.

        Precondition:
            2 <= max_depth <= 5
        """
        self.renderer = Renderer(num_human + random_players +
                                 len(smart_players))
        self.board = random_init(0, max_depth)
        self.board.update_block_locations((0, 0), BOARD_WIDTH)
        self.players = []

        # Choose a random goal
        if random.randint(1, 2) == 1:
            goal_type = 'blob'
        else:
            goal_type = 'perimeter'

        # Use the _generate_players helper method to create the players.
        # Iterate through the two following lists to insert the proper amount,
        # and type parameters into the method.
        player_types = ['human', 'random', 'smart']
        player_amounts = [num_human, random_players, len(smart_players)]
        for i in range(0, 3):
            # By using len(self.players) as the start_id for each batch of
            # players, it guarantees that the ids are consecutive and start
            # from 0.
            self.players.extend(self._generate_players(player_amounts[i],
                                                       player_types[i],
                                                       goal_type,
                                                       len(self.players)))
        # Set difficulties for SmartPlayers and display goals
        for player in self.players:
            if isinstance(player, SmartPlayer):
                player.difficulty = smart_players.pop()
            self.renderer.display_goal(player)

        self.renderer.draw(self.board, 0)

    def _generate_players(self, num_players: int,
                          player_type: str,
                          goal_type: str,
                          start_id: int) -> List[Player]:
        """Generate a list of players with the given number of players,
        of the given type, with the given <goal_type>, with ids incrementing
        from <start_id>.

        Preconditions:
            player_type == 'human', 'random', or 'smart'
            goal_type == 'blob', or 'perimeter'
        """
        player_list = []
        player_count = 0
        id_count = start_id

        while player_count < num_players:
            # Generate a blob goal or a perimeter goal with a random colour
            if goal_type == 'blob':
                goal = BlobGoal(COLOUR_LIST[random.randint(0, 3)])
            else:
                goal = PerimeterGoal(COLOUR_LIST[random.randint(0, 3)])

            # Generate a player of the given type, using goal
            if player_type == 'human':
                player = HumanPlayer(self.renderer, id_count, goal)
            elif player_type == 'random':
                player = RandomPlayer(self.renderer, id_count, goal)
            else:
                player = SmartPlayer(self.renderer, id_count, goal)

            # Add player to the player list, iterate counts by one
            player_list.append(player)
            player_count += 1
            id_count += 1

        return player_list


    def run_game(self, num_turns: int) -> None:
        """Run the game for the number of turns specified.

        Each player gets <num_turns> turns. The first player in self.players
        goes first.  Before each move, print to the console whose turn it is
        and what the turn number is.  After each move, print the current score
        of the player who just moved.

        Report player numbers and turn numbers using 1-based counting.
        For example, refer to the self.players[0] as 'Player 1'.

        When the game is over, print who won to the console.

        """
        # Index within self.players of the current player.
        index = 0
        for turn in range(num_turns * len(self.players)):
            player = self.players[index]
            print(f'Player {player.id}, turn {turn}')
            if self.players[index].make_move(self.board) == 1:
                break
            else:
                print(f'Player {player.id} CURRENT SCORE: ' +
                      f'{player.goal.score(self.board)}')
                index = (index + 1) % len(self.players)

        # Determine and report the winner.
        max_score = 0
        winning_player = 0
        for i in range(len(self.players)):
            score = self.players[i].goal.score(self.board)
            print(f'Player {i} : {score}')
            if score > max_score:
                max_score = score
                winning_player = i
        print(f'WINNER is Player {winning_player}!')
        print('Players had these goals:')
        for player in self.players:
            print(f'Player {player.id} ' +
                  f'goal = \n\t{player.goal.description()}: ' +
                  f'{colour_name(player.goal.colour)}')


def auto_game() -> None:
    """Run a game with two computer players of different difficulty.
    """
    random.seed(1001)
    game = Game(4, 0, 0, [1, 6])
    game.run_game(10)


def two_player_game() -> None:
    """Run a game with two human players.
    """
    random.seed(507)
    game = Game(2, 2, 0, [])
    game.run_game(5)


def solitaire_game() -> None:
    """Run a game with one human player.
    """
    random.seed(507)
    game = Game(4, 1, 0, [])
    game.run_game(10)


def sample_game() -> None:
    """Run a sample game with one human player, one random player,
    and one smart player.
    """
    # random.seed(1001)
    game = Game(5, 1, 1, [6])
    game.run_game(3)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['run_game'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
    })
    # sample_game()
    auto_game()
    # two_player_game()
    # solitaire_game()
