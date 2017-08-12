"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: Revise this function - right now it is the improved_score function now
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    own_center_score = custom_score_3(game, player)
    opp_center_score = custom_score_3(game,game.get_opponent(player))
    return float(own_moves - 2 * opp_moves + own_center_score - 2 * opp_center_score)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: Revise this funciton. Right now it is the open_move_score now
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: Revise this function. It is the center_score function now.
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)

def terminal_test(game):
    return len(game.get_legal_moves()) == 0

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=15.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        if terminal_test(game):
            return (-1,-1)
        else:
            best_move = game.get_legal_moves()[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.

                if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()
        a = moves[0]
        v = float("-inf")
        #print(game.get_legal_moves())
        for m in moves:
            contender = self.mm_value(game.forecast_move(m),depth-1, False)
            if contender > v:
                v = contender
                a = m
        #print("Next move is: ", next_move)
        return a

    def mm_value(self, game,depth, is_max):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if (depth == 0) | terminal_test(game):
            return self.score(game, self)
        if is_max:
            v = float("-inf")
        else:
            v = float("inf")
        for m in game.get_legal_moves():
            if is_max:
                v = max(v, self.mm_value(game.forecast_move(m),depth-1,False))
            else:
                v = min(v, self.mm_value(game.forecast_move(m),depth-1,True))
        return v

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        # I NEED TO ADD ITERATIVE DEEPENING HERE!
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        if terminal_test(game):
            return (-1,-1)
        else:
            best_move = game.get_legal_moves()[0]
        depth = 1
        #print("I am here")
        while True:
            #print("Now I'm in the while")
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_move = self.alphabeta(game, depth)
                depth += 1
                #print("At Depth ", depth, "Best Move is: ", best_move)

            except SearchTimeout:
                return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        v = float("-inf")
        moves = game.get_legal_moves()
        a = moves[0]
        #print(game.get_legal_moves())
        for m in moves:
            contender = self.ab_value(game.forecast_move(m),alpha,beta, depth-1, False)
            alpha = max(alpha,contender)
            if contender > v:
                v = contender
                a = m
        #print("Next move is: ", next_move)
        return a

    def ab_value(self, game,alpha, beta, depth, is_max):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if (depth == 0) | terminal_test(game):
            return self.score(game, self)
        if is_max:
            v = float("-inf")
        else:
            v = float("inf")
        for m in game.get_legal_moves():
            if is_max:
                v = max(v, self.ab_value(game.forecast_move(m),alpha,beta,depth-1,False))
                if v >= beta: return v
                alpha = max(alpha, v)
            else:
                v = min(v, self.ab_value(game.forecast_move(m),alpha,beta,depth-1,True))
                if v <= alpha: return v
                beta = min(beta, v)
        return v

if __name__ == "__main__":
    from isolation import Board

    # create an isolation board (by default 7x7)
    player1 = MinimaxPlayer()
    player2 = AlphaBetaPlayer()
    game = Board(player1, player2)

    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that the .apply_move() method changes the calling object in-place.

#    game.apply_move((3,3))
#    game.apply_move((3,4))
    game.apply_move(player1.get_move(game,lambda: 1))
#    game.apply_move((4,6))
    print(game.to_string())
#    game.apply_move(player1.get_move(game,lambda: 1000))
    game.apply_move(player2.get_move(game,lambda: 1))
    print(game.to_string())
    game.apply_move(player1.get_move(game,lambda: 1))
    print(game.to_string())
    game.apply_move(player2.get_move(game,lambda: 1))
    print(game.to_string())

#    game.apply_move(player1.get_move(game,2))
#    game.apply_move(player2.get_move(game,2))
#    print(game.to_string())

#    print(min_value(game))

    """
    game.apply_move(player1.get_move(game,10))
    game.apply_move(player2.get_move(game,10))
    print(game.to_string())

    game.apply_move(player1.get_move(game,10))
    game.apply_move(player2.get_move(game,10))
    print(game.to_string())
    print(terminal_test)

    game.apply_move(player1.get_move(game,10))
    game.apply_move(player2.get_move(game,10))
    print(game.to_string())

    game.apply_move(player1.get_move(game,10))
    game.apply_move(player2.get_move(game,10))
    print(game.to_string())

    assert(player1 == game.active_player)
    """
