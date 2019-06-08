#!/usr/bin/python3



# Question:
# Briefly describe how your program works, including any algorithms and data
# structures employed, and explain any design decisions you made along the way.

# Answer:
# As this game contains 2 players and every player place once in a turn,
# that we can choose the alphabeta tree to maximise our benefit.
#
# First, we need to give score to the CURRENT layout of the game in different
# situation. The score of mine is positive,
# and the score of another player is negative.
# From the nature of the game, 3 in a line (include diagonal) means win.
# If the movement will lead to winning, we give it a very large score. we win,
# then large positive score. Another player wins, a large absolute value of negative score.
# 2 in a line means, it's close to win. we give it a medium score.  we also prefer
# {1 0 1} than {1 1 0}.
# if two chees is blocked by another player's chess, we give it a (my turn ? 1 : -1) * score which absolue value is smaller than medium score.
# 1 in a line does not impact the game, 0 score.

# The quality of the score system matters, our strategy and predict are based on
# the score.


# Second, use alphabeta tree to recursively find the best move. It will go max_depth steps ahead, to find the max
# score of our turn and minimise the score when another player's placing.
# The advantage of this strategy is that we have also consider another player's best move.
#
# The alphabeta tree can accelerate the searching speed.
# Iterate current chessboard, try to place chess in every vacant position. Put it in the alphabeta tree to calculate
# the sum_score move.
# The sum_score of every current movement will represent the quality. It is clculated from max_depth steps ahead.
# The max from the sum_score is our next move.
#
# The total number of turns of this game is about 17(we counted). Our algorithm cannot go to
# this depth, because the speed will be too slow. The max_depth is set to 3 when it's the beginning
# of the game. And the largest max_depth is set to 7.

# In conclusion, actually our method is brute force, with alphabeta algorithm to speed up.



#!/usr/bin/python3
# Sample starter bot by Zac Partrige
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import numpy as np
import random

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   -1 - They played here


# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
curr = 0 # this is the current board to play in

# My board
# array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=int8)


# print a row
# This is just ported from game.c
def print_board_row(a, b, c, i, j, k):
    print("", boards[a][i], boards[a][j], boards[a][k], end=" | ")
    print(boards[b][i], boards[b][j], boards[b][k], end=" | ")
    print(boards[c][i], boards[c][j], boards[c][k])

# Print the entire board
# This is just ported from game.c
def print_board():
    print_board_row(1,2,3,1,2,3)
    print_board_row(1,2,3,4,5,6)
    print_board_row(1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(4,5,6,1,2,3)
    print_board_row(4,5,6,4,5,6)
    print_board_row(4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(7,8,9,1,2,3)
    print_board_row(7,8,9,4,5,6)
    print_board_row(7,8,9,7,8,9)
    print()

count_step = 0
# choose a move to play
def play():
    # print_board()

    # just play a random move for now
    # n = np.random.randint(1,9)
    # while boards[curr][n] != 0:
    #     n = np.random.randint(1,9)

    global count_step
    count_step += 1
    # print(count_step)

    n = my_turn(boards, curr)

    # print("playing", n)
    place(curr, n, 1)
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    # after I place the chess, curr change in order to locate the right subboard
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        # print(string)
        # print(string.split("("))
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), -1)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), -1)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), -1)
        return play()
    elif command == "win":
        print("Yey!! We win!! ")
        return -1
    elif command == "loss":
        print(" We lost")
        return -1
    return 0

#-------------
# if there are three cheeses in a line or diagnal, then win
win_situation = [
    [1, 2, 3],
	[4, 5, 6],
	[7, 8, 9],
	[1, 4, 7],
	[2, 5, 8],
	[3, 6, 9],
	[1, 5, 9],
	[3, 5, 7]
]

# the index of the list protentially_win means:
# The all situations can lead to win, if I place a chess in subboard[index]
protentially_win = [
    [win_situation[0], win_situation[3], win_situation[6]],
	[win_situation[0], win_situation[4]],
	[win_situation[0], win_situation[5], win_situation[7]],
	[win_situation[1], win_situation[3]],
	[win_situation[1], win_situation[4], win_situation[6], win_situation[7]],
	[win_situation[1], win_situation[5]],
	[win_situation[2], win_situation[3], win_situation[7]],
	[win_situation[2], win_situation[4]],
	[win_situation[2], win_situation[5], win_situation[6]]
]

# assume I have already placed my chess in position_to_place
# position_to_place is int from 1 to 9
def curr_score(board, curr, position_to_place):
    win = False
    # to adjust the index which starts from 1
    # position_to_place - 1

    # larger score means larger possibility to win
    score_to_win = 0
    # score_on_board is to evaluate the layout of the game
    for possible_win in protentially_win[position_to_place - 1]:
        score_on_board = board[curr][possible_win[0]] + board[curr][possible_win[1]] + board[curr][possible_win[2]]
        # 3 in a line, someone wins
        # it's a terminal node
        if score_on_board == 3 or score_on_board == -3:
            score_to_win = score_on_board * 100000
            win = True
            break
        # two in a line for me
        # And {x _ x} is better than {x x _}
        elif score_on_board == 2:
            score_to_win += 2000
            if board[curr][possible_win[1]] == 0:
                score_to_win += 500
        # two in a line for another player
        elif score_on_board == -2:
            score_to_win -= 2000
            if board[curr][possible_win[1]] == 0:
                score_to_win -= 500
        elif score_on_board == 1 or score_on_board == -1:
            # if I can block a win situation
            if board[curr][possible_win[0]] & board[curr][possible_win[1]] & board[curr][possible_win[2]]:
            #if board[curr][possible_win[0]] != 0 and board[curr][possible_win[1]] != 0 and board[curr][possible_win[2]] != 0:
                score_to_win -= score_on_board * 500

    return [score_to_win, win]


# pesudocode of the alphabeta_tree is in the slide

def alphabeta_tree(board, curr, player_cur, player_next, alpha, beta, score_sum, depth, max_depth, if_won):
    # return a val
    if depth >= max_depth or if_won:
        return score_sum

    for i in range(1, 10):
        if board[curr][i] == 0:
            board[curr][i] = player_cur
            score_cur = curr_score(board, curr, i)[0]
            if_won = curr_score(board, curr, i)[1]
            val = alphabeta_tree(board, i, player_next, player_cur, alpha, beta, score_cur + score_sum, depth + 1,  max_depth, if_won)
            board[curr][i] = 0

            if player_cur == 1:
                if val > alpha:
                    alpha = val
            else:
                if val < beta:
                    beta = val
            # pruning
            if beta <= alpha:
                break

    if player_cur == 1:
        return alpha
    return beta

# return my move in my turn
def my_turn(board, curr):
    global count_step
    search_depth = 3
    max_val = -float('inf')
    for i in range(1, 10):
        if board[curr][i] == 0:
            board[curr][i] = 1
            score_cur = curr_score(board, curr, i)[0]
            # current move
            if_won = curr_score(board, curr, i)[1]

            # put next subboard into the alphabeta tree,
            # next move is another player's move
            # early steps are not that important,
            # before step5, the search depth is 3
            # the max search depth is 7
            # if over 7, it will be too slow
            if count_step > 5:
                search_depth = 7

            val = alphabeta_tree(board, i, -1, 1, -float('inf'), float('inf'), score_cur, 1, search_depth, if_won)

            board[curr][i] = 0
            # find the best curr move
            if val > max_val:
                max_val = val
                my_move = [i]
            if val == max_val:
                my_move.append(i)
    return random.choice(my_move)


# connect to socket
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

        s.connect(('localhost', port))
        while True:
            text = s.recv(1024).decode()
            if not text:
                continue
            for line in text.split("\n"):
                response = parse(line)
                if response == -1:
                    return
                elif response > 0:
                    s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
