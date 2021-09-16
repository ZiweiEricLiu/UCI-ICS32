 #connectfour_console.py
#
# ICS 32 Spring 2018
# Project #2: Send Me On My Way

import connectfour
import connectfour_functions_for_UI

def _start_game() -> connectfour.GameState:
    '''start a new connectfour game, return a GameState object'''
    return connectfour.new_game()

def _print_turn(game_state: connectfour.GameState) -> None:
    '''print the turn to the users'''
    if game_state.turn == connectfour.RED: turn = 'RED'
    if game_state.turn == connectfour.YELLOW: turn = 'Yellow'
    print("--------------------------\nThis is {}'s turn\n".format(turn))
    return

def console() -> None:
    '''
    Displays the user interface to the user
    the game will end when someone wins
    '''
    game_state = _start_game()
    connectfour_functions_for_UI.welcome()
    while True:
        connectfour_functions_for_UI.print_board(game_state)
        _print_turn(game_state)
        try:
            move = connectfour_functions_for_UI.read_move()
            game_state = connectfour_functions_for_UI.drop_pop(game_state, move)
        except connectfour.InvalidMoveError:
            print('\nMove is not valie\nEither it is not in the correct format or the column you entered cannot do this move, please try again\n')
        except ValueError:
            print('\nMove is not valid, column number must be integer between 1 and {}\n'.format(connectfour.BOARD_COLUMNS))
        if connectfour_functions_for_UI.win(game_state):
            connectfour_functions_for_UI.print_board(game_state)
            break
    return

if __name__=='__main__':
    console()
