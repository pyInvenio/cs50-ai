"""
Tic Tac Toe Player
"""

import math, copy

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

from collections import Counter
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    c = Counter(list(y for x in board for y in x ))
    if X in c:
        if c[X] > c[O]:
            return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ret = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                ret.add((i,j))
    return ret


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    b = copy.deepcopy(board)
    if action not in actions(board):
        # print("result", action, actions(b), b)
        raise Exception("Invalid action")
    b[action[0]][action[1]] = player(b)
    return b


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if set(board[i]) == {X}:
            return X
        elif set(board[i]) == {O}:
            return O
    for j in range(3):
        if set(board[i][j] for i in range(3)) == {X}:
            return X
        elif set(board[i][j] for i in range(3)) == {O}:
            return O
    if set(board[i][i] for i in range(3)) == {X} or set(board[2-i][i] for i in range(3)) == {X}:
        return X
    if set(board[i][i] for i in range(3)) == {O} or set(board[2-i][i] for i in range(3)) == {O}:
        return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) is not None or (EMPTY not in set(y for x in board for y in x ) and winner(board) is None) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    def maxVal(b):
        if terminal(b):
            return (utility(b), None)
        v = float('-inf')
        act = None
        prevV = v
        
        for a in actions(b):
            # print("max", a, actions(b), b)
            v = max(v, minVal(result(b, a))[0])
            if v > prevV:
                act = a
                prevV = v
            if v == 1:
                return (v, act)
           
        return (v, act)
    def minVal(b):
        if terminal(b):
            return (utility(b), None)
        v = float('inf')
        act = None
        prevV = v
        for a in actions(b):
            # print("min", a, actions(b), b)

            v = min(v, maxVal(result(b, a))[0])
            
            if v < prevV:
                act = a
                prevV = v
            if v == -1:
                return (v, act)
            
        return (v, act)
    
    if player(board) == X:
        return maxVal(board)[1]
    else:
        return minVal(board)[1]
    
    