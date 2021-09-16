#connectfour_onlineUI
#
#ICS 32 Spring 2018
# Project #2: Send Me On My Way

import connectfour_socket
import connectfour
import connectfour_functions_for_UI

class ProtocolError(Exception):
    '''Raised whenever an protocol is not follwed'''
    pass

def _connect() -> 'connection':
    '''
    ask the user for a host and a port, and then connect to the server
    if successful, a connection object is returned; if unsuccessful, an
    exception is raised
    '''
    host = connectfour_socket.read_host()
    port = connectfour_socket.read_port()

    print('Connecting to host {} port {}...'.format(host,port))
    connection = connectfour_socket.connect(host,port)
    print('Connected')
    return connection

def _start_game(connection: 'connection') -> connectfour.GameState:
    '''
    start a new connectfour game, if sucessful, a GameState object is returned;
    if unsuccessful, a ProtocolError is raised
    '''
    name = connectfour_socket.read_name()
    connectfour_socket.write(connection, 'I32CFSP_HELLO ' + name)
    if connectfour_socket.read(connection) != 'WELCOME ' + name:
        raise ProtocolError()
    connectfour_socket.write(connection, 'AI_GAME')
    if connectfour_socket.read(connection) != 'READY':
        raise ProtocolError()
    game_state = connectfour.new_game()
    return game_state

def _read_server_move(connection: 'connection') -> str:
    '''
    return the move the server made
    '''
    move_status = connectfour_socket.read(connection)
    server_move = connectfour_socket.read(connection)
    ready = connectfour_socket.read(connection)
    return server_move
    
def user_interface() -> None:
    '''
    Displays the user interface to the user
    if any ProtocolError is catched, the connection to the server will close
    invalid moves from the user and server are also handled in the user interface
    the game will end when someone wins or a ProtocolError is catched
    '''
    try:
        while True:
            try:
                connection = _connect()
                break
            except:
                print('Cannot connect to the server, please check if the host and port are correct and try again')
        game_state = _start_game(connection)
                
        connectfour_functions_for_UI.welcome()

        while True:
            connectfour_functions_for_UI.print_board(game_state)
            try:
                move = connectfour_functions_for_UI.read_move()
                game_state = connectfour_functions_for_UI.drop_pop(game_state, move)
            except connectfour.InvalidMoveError:
                print('\nMove is not valie\nEither it is not in the correct format or the column you entered cannot do this move, please try again\n')
                continue
            except ValueError:
                print('\nMove is not valid, column number must be integer between 1 and {}\n'.format(connectfour.BOARD_COLUMNS))
                continue
            connectfour_socket.write(connection, move)
            print('Your make the move: {}'.format(move))
            connectfour_functions_for_UI.print_board(game_state)
            if connectfour_functions_for_UI.win(game_state):
                connectfour_functions_for_UI.print_board(game_state)
                break

            server_move = _read_server_move(connection)
            try:
                game_state = connectfour_functions_for_UI.drop_pop(game_state, server_move)
            except:
                print('The server made an invalid move, connection close')
                break
            print('Your opponent make the move: {}'.format(server_move))
            if connectfour_functions_for_UI.win(game_state):
                connectfour_functions_for_UI.print_board(game_state)
                break
    except ProtocolError:
        print('The server does not follow protocol,connection close')
    connectfour_socket.close(connection)

if __name__ == '__main__':
    user_interface()
