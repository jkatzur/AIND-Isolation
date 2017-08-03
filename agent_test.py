"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import importlib
import isolation
import game_agent

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

"""
    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        game.apply_move((6, 2))
        game.apply_move(player2.get_move(game,10))
        game.apply_move((5,4))
        game.apply_move(player2.get_move(game,10))
        game.apply_move((3,3))
        game.apply_move(player2.get_move(game,10))
        game.apply_move((4,5))
        game.apply_move(player2.get_move(game,10))
        game.apply_move((6,6))
        game.apply_move(player2.get_move(game,10))
        assert(terminal_test(game,game.active_player))
"""

if __name__ == '__main__':
    unittest.main()
