"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCounter = 0
    oCounter = 0

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                xCounter += 1
            elif board[i][j] == O:
                oCounter += 1

    if xCounter > oCounter:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Goes through the board and checks if any board position at (i,j) is empty, if it is, add it to the set()
    """
    possibleActions = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create new board, without modifying the original board received as input
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    if all(i == board[0][0] for i in board[0]):
        return board[0][0]
    elif all(i == board[1][0] for i in board[1]):
        return board[1][0]
    elif all(i == board[2][0] for i in board[2]):
        return board[2][0]
    # Check columns
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]
    # Check diagonals
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None):
        return True
    else:
        return False
    #return True if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None) else False # noqa E501


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    # Check how to handle exception when a non terminal board is received.


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    move = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        aux, act = min_value(result(board, action))
        if aux > v:
            v = aux
            move = action
            if v == 1:
                return v, move

    return v, move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    move = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        aux, act = max_value(result(board, action))
        if aux < v:
            v = aux
            move = action
            if v == -1:
                return v, move

    return v, move

def random_move(board):
    """
    Returns a random action (i, j) available on the board.
    """
    possible_actions = actions(board)
    return random.choice(list(possible_actions))


class Node:
    def __init__(self, board, parent=None, action=None):
        self.board = board
        self.parent = parent
        self.action = action
        self.children = []
        self.wins = 0
        self.visits = 0

    def is_terminal(self):
        return terminal(self.board)

    def is_fully_expanded(self):
        return len(self.children) == len(actions(self.board))

    def select_child(self):
        """
        Selects a child node based on the Upper Confidence Bound for Trees (UCT) formula.
        """
        exploration_constant = 1.4  # Tunable parameter
        return max(self.children, key=lambda child: child.wins / child.visits + exploration_constant * math.sqrt(
            math.log(self.visits) / child.visits))

    def expand(self):
        """
        Expands the current node by adding a child node corresponding to an untried action.
        """
        untried_actions = actions(self.board) - {child.action for child in self.children}
        action = random.choice(list(untried_actions))
        new_board = result(self.board, action)
        new_child = Node(new_board, parent=self, action=action)
        self.children.append(new_child)
        return new_child

    def simulate(self):
        """
        Simulates a random game from the current node to the end.
        Returns the winner of the simulated game.
        """
        board_copy = copy.deepcopy(self.board)
        current_player = player(board_copy)
        while not terminal(board_copy):
            action = random_move(board_copy)
            board_copy = result(board_copy, action)
            current_player = player(board_copy)
        return utility(board_copy)

    def update(self, winner):
        """
        Updates the node's wins and visits statistics based on the result of a simulated game.
        """
        self.visits += 1
        if winner == 1:
            self.wins += 1

    def get_best_action(self):
        """
        Returns the action that leads to the child node with the highest number of visits.
        """
        return max(self.children, key=lambda child: child.visits).action


def monte_carlo_tree_search(board, iterations):
    """
    Performs Monte Carlo Tree Search on the Tic Tac Toe board for a certain number of iterations.
    Returns the best action found after the specified iterations.
    """
    root = Node(board)

    for _ in range(iterations):
        node = root
        # Selection
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.select_child()

        # Expansion
        if not node.is_terminal():
            node = node.expand()

        # Simulation
        winner = node.simulate()

        # Backpropagation
        while node is not None:
            node.update(winner)
            node = node.parent

    return root.get_best_action()