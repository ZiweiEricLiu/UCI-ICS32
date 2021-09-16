import pygame
import column_logic
import random

#These two constants are the row and column of the game
ROW_NUM = 13
COLUMN_NUM = 6

class ColumnGame:
    '''
    This is a class represents the user interface of the column game,
    which displays tha game
    '''
    def __init__(self):
        self._running = True
        self._state = column_logic.GameState(ROW_NUM, COLUMN_NUM)
    def run(self) -> None:
        '''
        This function runs the program, displaying the graphic user interface
        '''
        pygame.init()

        self._resize_surface((600,780))

        clock = pygame.time.Clock()
        
        while self._running:
            counter = 0
            interval = 5
            while counter < interval:
                if self._state.faller_pos == None:
                    self._insert_a_faller()
                clock.tick(9)
                self._handle_events()
                self._redraw()
                counter += 1
            self._state.one_tick()
            while self._state.match == True:
                clock.tick(9)
                self._redraw()
                self._state.one_tick()
                
            if self._state.game_over == True:
                self._end_game()

        pygame.quit()

    def _handle_events(self) -> None:
        '''
        This function handle the events that can happen when the user does
        certain operations
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._state.move_left()
                if event.key == pygame.K_RIGHT:
                   self._state.move_right()
                if event.key == pygame.K_SPACE:
                    self._state.rotate() 

    def _draw_background(self) -> None:
        '''
        Draw the background on the display
        '''
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()

        left_frac_x = 0
        right_frac_x = 0.8
        width_frac = 0.2
        height_frac = 1
        
        pygame.draw.rect(surface, pygame.Color(123,123,123), pygame.Rect((0,0),(width_frac*width,height)))
        pygame.draw.rect(surface, pygame.Color(123,123,123), pygame.Rect((right_frac_x*width,0),(width_frac*width,height)))

    def _draw_gems(self, game_state: column_logic.GameState) -> None:
        '''
        Draw the gems on the display
        '''
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        
        for r in range(ROW_NUM):
            for c in range(COLUMN_NUM):
                gem = self._state.get_gem_from_board(r,c)
                if gem != None:
                    color = self._handle_gem_color(gem)
                    top_left_frac_x = 0.2+0.1*c
                    top_left_frac_y = 0.077*r
                    width_frac = 0.16667
                    height_frac = 0.077
                    background_width = 0.4*width
                    
                    display_rect = pygame.Rect((top_left_frac_x*width, top_left_frac_y*height),
                                               (width_frac*(width-background_width),height_frac*height))
                    pygame.draw.rect(surface, color, display_rect)

    def _handle_gem_color(self, gem: column_logic.Gem) -> pygame.Color:
        '''
        This function reads the Gem object's color, which is a string
        and returns a Color object relative to the Gem's color
        This function also handles the color of the gem when it is landed and matched
        '''
        if gem.status == column_logic.LANDED:
            if gem.color == 'S':
                return pygame.Color(255-60,0,0)
            if gem.color == 'T':
                return pygame.Color(182-60,102-60,0)
            if gem.color == 'V':
                return pygame.Color(85-60,122-60,0)
            if gem.color == 'W':
                return pygame.Color(0, 150-60,150-60)
            if gem.color == 'X':
                return pygame.Color(0,0,223-60)
            if gem.color == 'Y':
                return pygame.Color(173-60,0,77)
            if gem.color == 'Z':
                return pygame.Color(0,255-60,0)
        elif gem.status == column_logic.MATCH:
            return pygame.Color(0,0,0)
        else:
            if gem.color == 'S':
                return pygame.Color(235,0,0)
            if gem.color == 'T':
                return pygame.Color(162,82,3)
            if gem.color == 'V':
                return pygame.Color(65,102,0)
            if gem.color == 'W':
                return pygame.Color(0, 130,130)
            if gem.color == 'X':
                return pygame.Color(0,33,203)
            if gem.color == 'Y':
                return pygame.Color(153,0,77)
            if gem.color == 'Z':
                return pygame.Color(0,235,0)
        
    def _redraw(self) -> None:
        '''
        This function redraw the display in order to update the state of the game
        '''
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(255,255,255))

        self._draw_background()

        self._draw_gems(self._state)
                         
        pygame.display.flip()

    def _insert_a_faller(self) -> None:
        '''
        This function randomly create faller when there is no faller on the display
        '''
        random_column = round(random.random()*5)
        random_gems = []
        for i in range(3):
            random_gems.append(column_logic.Gem(column_logic.VALID_COLORS[round(random.random()*6)],column_logic.FALLER))
        self._state.create_a_faller(random_column, random_gems)
        
    def _end_game(self) -> None:
        '''
        This function changes the indicator of whether the game should keep running to False
        '''
        self._running = False

    def _resize_surface(self, size: (int, int)) -> None:
        '''
        This function takes in a size of the display
        and resizes the display to that size
        '''
        pygame.display.set_mode(size, pygame.RESIZABLE)

if __name__ == '__main__':
    ColumnGame().run()
