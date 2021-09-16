# column_ui.py

#Name: Eric Liu
#StudentID: 56277704

import column_logic

def ask_start() -> ('row','col','mode'):
    '''
    ask the user for details (row,col,mode) to start the game
    return a tuple of user inputs
    '''
    return input(), input(), input()

def ask_command() -> str:
    '''
    ask the user for command
    return a string of user input
    '''
    return input()

def _ask_contents(row:int, col:int) -> 'Contents':
    '''
    ask the user for contents to start the game if CONTENTS mode is selected
    return a list of contents
    '''
    contents_list = []
    for i in range(row):
        contents_list.append(input()[0:col])
    return contents_list

def start(begin_options: tuple) -> column_logic.GameState:
    '''
    initialize the game by taking in details (row, col, mode)
    return a GameState Object
    '''
    row = int(begin_options[0])
    col = int(begin_options[1])
    mode = begin_options[2]
    game_state = column_logic.GameState(row, col)
    if mode == 'EMPTY':
        return game_state
    elif mode == 'CONTENTS':
        contents = _ask_contents(row, col)
        game_state.fill_with_contents(contents)
        return game_state

def command_handle(cmd: str, game_state: column_logic.GameState) -> None:
    '''
    Handle the command the user inputs
    Raise an Exception if the command is not valid
    '''
    if cmd == '':
        game_state.one_tick()
    elif cmd[0] == 'F':
        cmd_list = cmd.split()
        gems = []
        for gem in cmd_list[2:]:
            gems.append(column_logic.Gem(gem, column_logic.FALLER))
        game_state.create_a_faller(int(cmd_list[1])-1, gems)
    elif cmd == 'R':
        game_state.rotate()
    elif cmd == '>':
        game_state.move_right()
    elif cmd == '<':
        game_state.move_left()
    else:
        raise CommandIsNotValidError()
    
def print_board(game_state: column_logic.GameState) -> None:
    '''
    print the game board
    '''
    game_state.print()

def is_game_over(game_state: column_logic.GameState) -> bool:
    '''Return True if the game is over otherwise return Flase'''
    return game_state.game_over                     

def run():
    '''
    Execute the game
    '''
    game_state = start(ask_start())
    
    while not is_game_over(game_state):
        print_board(game_state)
        command = ask_command()
        if command == 'Q':
            return
        command_handle(command, game_state)
        
    print_board(game_state)
    print('GAME OVER')

class CommandIsNotValidError(Exception):
    '''Raise when the command is not valid'''
    pass

if __name__ == '__main__':
    run()
