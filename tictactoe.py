"""
Tic Tac Toe Player
"""

import random
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    # return [[EMPTY, EMPTY, EMPTY],
    #         [EMPTY, EMPTY, EMPTY],
    #         [EMPTY, EMPTY, EMPTY]]
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # use p1 to denote how many X are in the board
    # use p2 to denote how many O are in the board
    p1 = 0
    p2 = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                p1 += 1
            elif board[i][j] == O:
                p2 += 1
    # since X moves first, p1 won't be less than p2
    # p1 == p2: next is X
    # p1 > p2: next is O
    return X if p1 == p2 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # iterate through the board to find EMPTY spot
    act = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                act.add((i, j))
    # will return None if the game ended in a tie
    return act


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # get a set of all possible actions (i, j)
    act_set = actions(board)
    # raise exception if not a valid action
    if action not in act_set:
        raise NameError('illegal action')
    # make a deep copy of the original board and mark the move
    new_board = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    new_board[i][j] = X if player(board) == X else O
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # use number to mark the board: [[0,1,2],[3,4,5],[6,7,8]]
    # use x_set and o_set to mark each player's chess on the board
    x_set = set()
    o_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_set.add(i * 3 + j)
            elif board[i][j] == O:
                o_set.add(i * 3 + j)
    # list all possible winning combination
    win_set = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
               {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]
    # check whether x_set or o_set contains a winning combination
    for win in win_set:
        if win.issubset(x_set):
            return X
        if win.issubset(o_set):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if someone has won the game: end
    if not (winner(board) is None):
        return True
    # if no one has won, and there's empty space in the board:
    # the game goes on
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    # end in a tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # return None if is a terminal board
    if terminal(board):
        return None
    # applying alpha-beta pruning with a helper function
    alpha = float("-Infinity")
    beta = float("Infinity")
    return minimax_helper(board, alpha, beta)[0]


def minimax_helper(board, alpha, beta):
    """
    Input:
    board: the board status
    alpha: the lower bound
    beta: the upper bound

    Return:
    the optimal action and its corresponding score
    for the current player on the board.
    """
    # get a set of all possible actions
    act_set = actions(board)
    # if it is the first move: choose randomly on the board
    if len(act_set) == 9:
        i = random.randint(0, 2)
        j = random.randint(0, 2)
        return (i, j), None
    # not first move, initiate best score
    best_score = float("-Infinity") if player(board) == X \
        else float("Infinity")

    # check each possible action:
    for act in act_set:
        new_board = result(board, act)
        # base case: game ends, return the utility
        if terminal(new_board):
            return act, utility(new_board)
        # check the highest possible score for this action
        _, new_score = \
            minimax_helper(new_board, alpha, beta)

        # X is making decision, try to maximize:
        if player(board) == X:
            # if gets a higher point than current best:
            if new_score > best_score:
                best_act = act
                best_score = new_score
                # update the lower bound alpha(this level, maximizing)
                # upper bond beta(upper level, minimizing) unchanged
                alpha = new_score
        # O is making decision, try to minimize:
        else:
            # if gets a lower point than current best:
            if new_score < best_score:
                best_act = act
                best_score = new_score
                # update the upper bound beta(this level, minimizing)
                # lower bond alpha(upper level, maximizing) unchanged
                beta = new_score

        # if lower bound is bigger than upper bound: pruning
        if alpha >= beta:
            break

    return best_act, best_score

# # %%
# def initial_state():
#     """
#     Returns starting state of the board.
#     """
#     # return [[EMPTY, EMPTY, EMPTY],
#     #         [EMPTY, EMPTY, EMPTY],
#     #         [EMPTY, EMPTY, EMPTY]]
#     return [[EMPTY, EMPTY, X],
#             [EMPTY, EMPTY, EMPTY],
#             [EMPTY, O, X]]


# s=initial_state()
# # %%
# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     # return None if is a terminal board
#     if terminal(board):
#         return None
#     # applying alpha-beta pruning with a helper function

#     return minimax_helper(board)


# def minimax_helper(board):
#     """
#     Input:
#     board: the board status
#     alpha: the lower bound
#     beta: the upper bound

#     Return:
#     the optimal action and its corresponding score
#     for the current player on the board.
#     """
#     # get a set of all possible actions
#     act_set = actions(board)
#     # if it is the first move: choose randomly on the board
#     if len(act_set) == 9:
#         i = random.randint(0, 2)
#         j = random.randint(0, 2)
#         return (i, j), None
#     # not first move, initiate best score
#     best_score = float("-Infinity") if player(board) == X \
#         else float("Infinity")

#     # check each possible action:'
#     for act in act_set:
#         new_board = result(board, act)
#         # base case: game ends, return the utility
#         if terminal(new_board):
#             return act, utility(new_board)
#         # check the highest possible score for this action
#         _, new_score = \
#             minimax_helper(new_board)

#         # X is making decision, try to maximize:
#         if player(board) == X:
#             # if gets a higher point than current best:
#             if new_score > best_score:
#                 best_act = act
#                 best_score = new_score
#                 # update the lower bound alpha(this level, maximizing)
#                 # upper bond beta(upper level, minimizing) unchanged

#         # O is making decision, try to minimize:
#         else:
#             # if gets a lower point than current best:
#             if new_score < best_score:
#                 best_act = act
#                 best_score = new_score
#                 # update the upper bound beta(this level, minimizing)


#     return best_act, best_score
# # %%
# minimax(s)
# # %%
