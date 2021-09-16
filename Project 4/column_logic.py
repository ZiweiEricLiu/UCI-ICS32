# column_logic.py

#Name: Eric Liu
#StudentID: 56277704

import collections

# These constants specify the concepts of the status of the Gems
FROZEN = 0
FALLER = 1
LANDED = 2
MATCH = 3

# This constant specify the valid colors that can be used for the Gems
VALID_COLORS = 'STVWXYZ'

class GameState:
    '''
    GameState is a class that tracks everything important about the state
    of a Column game as it progresses
    '''
    
    def __init__(self, row:int, col:int):
        '''
        this constructor initilizes the game by taking in two parameters
        the row and the col of the game board
        '''
        self.board = []
        self.row = row
        self.col = col
        self.faller_pos = None
        self.match = False
        self.game_over = False
        for r in range(row+2):
            self.board.append([])
            for c in range(col):
                self.board[-1].append(None)

    def get_gem_from_board(self, row:int, col:int) -> 'Gem':
        '''
        this function return a Gem object that is on the board
        with the specific row and column
        '''
        return self.board[row+2][col]
    
    def fill_with_contents(self, contents: [str]) -> None:
        '''
        this function fills the board with desired contents if CONTENTS mode
        is chosen
        it takes in a list of string which represents the contents
        '''
        for r in range(self.row):
            temp_row = []
            for c in range(self.col):
                if contents[r][c] == ' ':
                    temp_row.append(None)
                else:
                    temp_row.append(Gem(contents[r][c], FROZEN))
            self.board[r+2] = temp_row
        self._fall_all_gems_to_bottom()

    def _fall_all_gems_to_bottom(self) -> None:
        '''
        this function is called after the CONTENTS game is set up or after
        matched gems disappear to let all the gems fall to bottom if they can
        '''
        for r in range(self.row, -1, -1):
            for c in range(self.col):
                if self.board[r][c] != None:
                    counter = r
                    while counter<=self.row and self.board[counter+1][c] == None:
                        self.board[counter+1][c] = self.board[counter][c]
                        self.board[counter][c] = None
                        counter += 1
        for r in range(self.row+1, 1, -1):
            for c in range(self.col):
                if self._is_match(self.board, c, r):
                    self.board[r][c].change_status(MATCH)
                    self.match = True
                    
    def one_tick(self) -> None:
        '''
        this function let the state of the game to progress one tick
        '''
        disappear_happening = False
        for r in range(self.row+1, -1, -1):
            for c in range(self.col):
                if self.board[r][c] != None:
                    if self.board[r][c].status == FROZEN:
                        continue
                    elif self.board[r][c].status == FALLER:
                        if self.board[r+1][c] == None:
                            self.board[r+1][c] = self.board[r][c]
                            self.board[r][c] = None
                            if r == self.faller_pos[0] and c == self.faller_pos[1]:
                                self.faller_pos = [r+1,c]
                            if r+1>self.row or self.board[r+2][c] != None and self.board[r+2][c].status != FALLER:
                                self.board[r+1][c].change_status(LANDED)
                    elif self.board[r][c].status == LANDED:
                            self.board[r][c].change_status(FROZEN)
                            self.faller_pos = None
                    elif self.board[r][c].status == MATCH:
                        disappear_happening = True
                        self.match = False
                        self.board[r][c] = None
        if self.faller_pos == None:
            for r in range(self.row+1, 1, -1):
                for c in range(self.col):
                    if self._is_match(self.board, c, r):
                        self.board[r][c].change_status(MATCH)
                        self.match = True
        if disappear_happening:
            self._fall_all_gems_to_bottom()
            
        if self._is_game_over():
            self.game_over = True

    def _is_match(self, board: [[int]], col: int, row: int) -> bool:
        '''
        Returns True if a sequence of gems is matched
        '''
        return self._three_in_a_row(board, col, row, 0, 1) \
                or self._three_in_a_row(board, col, row, 1, 1) \
                or self._three_in_a_row(board, col, row, 1, 0) \
                or self._three_in_a_row(board, col, row, 1, -1) \
                or self._three_in_a_row(board, col, row, 0, -1) \
                or self._three_in_a_row(board, col, row, -1, -1) \
                or self._three_in_a_row(board, col, row, -1, 0) \
                or self._three_in_a_row(board, col, row, -1, 1)\
                or self._mid_in_a_row(board, col, row, 0, 1)\
                or self._mid_in_a_row(board, col, row, 1, 0)\
                or self._mid_in_a_row(board, col, row, 1, 1)\
                or self._mid_in_a_row(board, col, row, 1, -1)

    def _mid_in_a_row(self, board: [[int]], col: int, row: int, coldelta: int, rowdelta: int) -> bool:
        '''
        Returns True if the gem between two gems is matched
        '''
        start_gem = board[row][col]

        if start_gem == None:
            return False
        else:
            for i in [-1, 1]:
                if not self._is_valid_column_number(col + coldelta * i) \
                        or not self._is_valid_row_number(row + rowdelta * i)\
                        or board[row + rowdelta * i][col + coldelta *i] == None\
                        or board[row + rowdelta * i][col + coldelta *i].color != start_gem. color:
                    return False
            return True
        
    def _three_in_a_row(self, board: [[int]], col: int, row: int, coldelta: int, rowdelta: int) -> bool:
        '''
        Returns True if a gem beginning in the given column and row
        is matched to gems that are in a extending direction
        specified by the coldelta and rowdelta
        '''
        start_gem = board[row][col]

        if start_gem == None:
            return False
        else:
            for i in range(1, 3):
                if not self._is_valid_column_number(col + coldelta * i) \
                        or not self._is_valid_row_number(row + rowdelta * i)\
                        or board[row + rowdelta * i][col + coldelta *i] == None\
                        or board[row + rowdelta * i][col + coldelta *i].color != start_gem. color:
                    return False
            return True

    def _is_valid_column_number(self, col: int) -> bool:
        '''
        return True if the input column is valid
        '''
        if col > self.col-1 or col < 0:
            return False
        else:
            return True

    def _is_valid_row_number(self, row: int) -> bool:
        '''
        return True if the input row is valid
        '''
        if row > self.row+1 or row < 2:
            return False
        else:
            return True
        
    def create_a_faller(self, col:int, gems:list) -> None:
        '''
        Create a faller in a specified column with specified list of gems
        '''
        if self.board[2][col] != None:
            self.game_over = True
        else:
            self.board[0][col] = gems[0]
            self.board[1][col] = gems[1]
            self.board[2][col] = gems[2]
            self.faller_pos = [2,col]
            if self.board[3][col] != None:
                self.board[0][col].change_status(LANDED)
                self.board[1][col].change_status(LANDED)
                self.board[2][col].change_status(LANDED)

    def rotate(self) -> None:
        '''
        Rotate the faller
        '''
        if self.faller_pos == None:
            return
        bottom_faller_row = self.faller_pos[0]
        bottom_faller_col = self.faller_pos[1]
        self.board[bottom_faller_row][bottom_faller_col],\
            self.board[bottom_faller_row-1][bottom_faller_col],\
            self.board[bottom_faller_row-2][bottom_faller_col] =\
            self.board[bottom_faller_row-1][bottom_faller_col],\
            self.board[bottom_faller_row-2][bottom_faller_col],\
            self.board[bottom_faller_row][bottom_faller_col]

    def move_left(self) -> None:
        '''
        Move the faller to one column left
        '''
        if self.faller_pos == None:
            return
        bottom_faller_row = self.faller_pos[0]
        bottom_faller_col = self.faller_pos[1]
        if not self._is_valid_column_number(bottom_faller_col-1)\
           or self.board[bottom_faller_row][bottom_faller_col-1] != None:
            return
        self.board[bottom_faller_row][bottom_faller_col-1],\
            self.board[bottom_faller_row-1][bottom_faller_col-1],\
            self.board[bottom_faller_row-2][bottom_faller_col-1] =\
            self.board[bottom_faller_row][bottom_faller_col],\
            self.board[bottom_faller_row-1][bottom_faller_col],\
            self.board[bottom_faller_row-2][bottom_faller_col],\

        self.board[bottom_faller_row][bottom_faller_col],\
            self.board[bottom_faller_row-1][bottom_faller_col],\
            self.board[bottom_faller_row-2][bottom_faller_col] =\
            None,None,None
        
        self.faller_pos = [bottom_faller_row,bottom_faller_col-1]

        if self.board[bottom_faller_row][bottom_faller_col-1].status == LANDED:
            if self._is_valid_row_number(bottom_faller_row+1)\
            and self.board[bottom_faller_row+1][bottom_faller_col-1] == None:
                self.board[bottom_faller_row][bottom_faller_col-1].change_status(FALLER)
                self.board[bottom_faller_row-1][bottom_faller_col-1].change_status(FALLER)
                self.board[bottom_faller_row-2][bottom_faller_col-1].change_status(FALLER)
        else:
            if self.board[bottom_faller_row+1][bottom_faller_col-1] != None:
                self.board[bottom_faller_row][bottom_faller_col-1].change_status(LANDED)
                self.board[bottom_faller_row-1][bottom_faller_col-1].change_status(LANDED)
                self.board[bottom_faller_row-2][bottom_faller_col-1].change_status(LANDED)

    def move_right(self) -> None:
        '''
        Move the faller to one column right
        '''
        if self.faller_pos == None:
            return
        bottom_faller_row = self.faller_pos[0]
        bottom_faller_col = self.faller_pos[1]
        if not self._is_valid_column_number(bottom_faller_col+1)\
           or self.board[bottom_faller_row][bottom_faller_col+1] != None:
            return
        self.board[bottom_faller_row][bottom_faller_col+1],\
            self.board[bottom_faller_row-1][bottom_faller_col+1],\
            self.board[bottom_faller_row-2][bottom_faller_col+1] =\
            self.board[bottom_faller_row][bottom_faller_col],\
            self.board[bottom_faller_row-1][bottom_faller_col],\
            self.board[bottom_faller_row-2][bottom_faller_col],\

        self.board[bottom_faller_row][bottom_faller_col],\
            self.board[bottom_faller_row-1][bottom_faller_col],\
            self.board[bottom_faller_row-2][bottom_faller_col] =\
            None,None,None
        
        self.faller_pos = [bottom_faller_row, bottom_faller_col+1]

        if self.board[bottom_faller_row][bottom_faller_col+1].status == LANDED:
            if self._is_valid_row_number(bottom_faller_row+1)\
            and self.board[bottom_faller_row+1][bottom_faller_col+1] == None:
                self.board[bottom_faller_row][bottom_faller_col+1].change_status(FALLER)
                self.board[bottom_faller_row-1][bottom_faller_col+1].change_status(FALLER)
                self.board[bottom_faller_row-2][bottom_faller_col+1].change_status(FALLER)
        else:
            if self.board[bottom_faller_row+1][bottom_faller_col+1] != None:
                self.board[bottom_faller_row][bottom_faller_col+1].change_status(LANDED)
                self.board[bottom_faller_row-1][bottom_faller_col+1].change_status(LANDED)
                self.board[bottom_faller_row-2][bottom_faller_col+1].change_status(LANDED)

    def _is_game_over(self) -> bool:
        '''
        return True if the game is over
        otherwise return False
        '''
        for r in range(2):
            for c in range(self.col):
                if self.board[r][c] != None:
                    if self.board[r][c].status == FROZEN and not self.match:
                        return True
        return False
    
    def print(self) -> None:
        '''
        print the game board
        '''
        for r in range(self.row):
            print('|',end='')
            for c in range(self.col):
                if self.board[r+2][c] == None:
                    print('   ', end='')
                else:
                    self.board[r+2][c].print()
            print('|')
        print(' ' + '---'*self.col + ' ')
                    
            
class Gem:
    '''
    Gem is a class that contains information, color and status, of a Gem Object
    '''
    def __init__(self, color: str, status: int):
        '''
        Initilize the color and status of the Gem
        '''
        if color in VALID_COLORS: 
            self.color = color
            self.status = status
        else:
            raise ColorIsNotValidError()

    def change_status(self, new_status: int) -> None:
        '''
        change the status of the Gem
        '''
        self.status = new_status
    def print(self) -> None:
        '''
        print the Gem
        '''
        if self.status == FROZEN:
            print(' '+self.color+' ', end='')
        elif self.status == FALLER:
            print('['+self.color+']', end='')
        elif self.status == LANDED:
            print('|'+self.color+'|', end='')
        elif self.status == MATCH:
            print('*'+self.color+'*', end='')

class ColorIsNotValidError(Exception):
    '''
    Raise when the color of the Gem is not valid when constructing
    '''
    pass

