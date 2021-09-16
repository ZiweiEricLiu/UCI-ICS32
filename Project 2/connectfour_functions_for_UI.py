#connectfour_functions_for_UI
#
#ICS 32 Spring 2018
# Project #2: Send Me On My Way

import connectfour

def print_board(game_state: connectfour.GameState) -> None:
    '''print the board of the current state to the users'''
    for i in range(1,connectfour.BOARD_COLUMNS):
        print(i, end=' ')
    print(connectfour.BOARD_COLUMNS)

    for row in range(connectfour.BOARD_ROWS):
        for col in range(connectfour.BOARD_COLUMNS-1):
            if game_state.board[col][row] == connectfour.NONE:
                print('.', end=' ')
            elif game_state.board[col][row] == connectfour.RED:
                print('R', end=' ')
            elif game_state.board[col][row] == connectfour.YELLOW:
                print('Y', end=' ')
        if game_state.board[connectfour.BOARD_COLUMNS-1][row] == connectfour.NONE:
            print('.')
        elif game_state.board[connectfour.BOARD_COLUMNS-1][row] == connectfour.RED:
            print('R')
        elif game_state.board[connectfour.BOARD_COLUMNS-1][row] == connectfour.YELLOW:
            print('Y')

def read_move() -> str:
    '''
    ask the user what move he wants to place, the input of the user must follow
    this format: DROP or POP followed by a (or more) space(s) followed by the
    column number (e.g. DROP 1 or POP 2 or DROP   1)
    Finally, reduce the spaces between the action and the column number to one
    space (to satisfy the protocol for 132CFSP) from the move, and return the move
    (e.g. user input DROP   1, this function will return DROP 1)
    '''
    move = input("Please enter a move in the format of DROP or POP followed by a (or more) space(s) followed by the column number (e.g. DROP 1 or POP 2): ")
    if len(move.split()) == 2:
        return move.split()[0] + ' ' + move.split()[1]
    else:
        raise connectfour.InvalidMoveError

def drop_pop(game_state: connectfour.GameState, move: str) -> connectfour.GameState:
    '''return a GameState object after after the user places a specific move'''
    if move.split()[0] == 'DROP':
        return connectfour.drop(game_state, int(move.split()[1])-1)
    elif move.split()[0] == 'POP':
        return connectfour.pop(game_state, int(move.split()[1])-1)
    else: raise connectfour.InvalidError

def win(game_state: connectfour.GameState) -> bool:
    '''
    return a True if someone wins and print the winner to the users
    otherwise return False
    '''
    if connectfour.winner(game_state) == connectfour.RED:
        print("------------------\nRED is the winner!\n------------------\n")
        return True
    if connectfour.winner(game_state) == connectfour.YELLOW:
        print("------------------\nYELLOW is the winner!\n------------------\n")
        return True
    else: return False


def welcome() -> None:
    '''print a welcome statement to the user'''
    print('------------------\nWelcome to connectfour!\n------------------\n')
