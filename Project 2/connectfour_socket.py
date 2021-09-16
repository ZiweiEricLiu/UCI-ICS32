#connectfour_socket
#
#ICS 32 Spring 2018
# Project #2: Send Me On My Way

import socket

def read_host() -> str:
    '''
    Asks the user to specify what host they'd like to connect to,
    continuing to ask until a valid answer is given.  An answer is
    considered valid when it consists of something other than just
    spaces.
    '''
    while True:
        host = input('Please enter the host: ')
        if host == '':
            print('Please enter a host (either a name or an IP address)')
        else:
            return host

def read_port() -> int:
    '''
    Asks the user to specify what port they'd like to connect to,
    continuing to ask until a valid answer is given.  A port must be an
    integer between 0 and 65535.
    '''
    while True:
        try:
            port = int(input('Please enter the port: '))
            if port < 0 or port > 65535:
                print('Ports must be an integer between 0 and 65535')
            else:
                return port
        except ValueError:
            print('Ports must be an integer between 0 and 65535')

def read_name() -> str:
    '''
    Asks the user to specify what their name is,
    continuing to ask until a valid answer is given.  A name cannot
    contain any whitespaces (space or tab)
    '''
    while True:
        name = input('Please enter your name: ')
        if ' ' in name or '\t' in name:
            print('Name cannot contain whitespace characters.')
        else:
            return name

def connect(host: str, port: int) -> 'connection':
    '''
    Connects to the echo server, which is assumed to be running on the
    given host and listening on the given port.  If successful, a
    connection object is returned; if unsuccessful, an exception is
    raised.
    '''
    echo_socket = socket.socket()
    echo_socket.connect((host, port))
    echo_socket_input = echo_socket.makefile('r')
    echo_socket_output = echo_socket.makefile('w')

    return echo_socket, echo_socket_input, echo_socket_output

def close(connection: 'connection') -> None:
    '''
    Closes a connection
    '''
    echo_socket, echo_socket_input, echo_socket_output = connection
    echo_socket_input.close()
    echo_socket_output.close()
    echo_socket.close()

def write(connection: 'connection', message: str) -> None:
    '''
    Sends a message to the server via a connection that is already
    assumed to have been opened (and not yet closed).
    '''
    echo_socket, echo_socket_input, echo_socket_output = connection
    echo_socket_output.write(message + '\r\n')
    echo_socket_output.flush()

def read(connection: 'connection') -> None:
    '''
    Receives a response from the server via a connection that is
    already assumed to have been opened (and not yet closed).
    '''
    echo_socket, echo_socket_input, echo_socket_output = connection
    return echo_socket_input.readline()[:-1]
