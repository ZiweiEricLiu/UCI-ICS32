# test_column_logic.py

#Name: Eric Liu
#StudentID: 56277704

import unittest
from column_logic import *

class ColumnTest(unittest.TestCase):
    
    def test_new_game_have_correct_column(self):
        new_game_state = GameState(4, 3)
        self.assertEqual(new_game_state.col, 3)

    def test_new_game_have_correct_row(self):
        new_game_state = GameState(4, 3)
        self.assertEqual(new_game_state.row, 4)

    def test_new_contents_game_have_correct_jewels(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents([' X ', '   ', '   ', 'X X'])
        self.assertEqual(new_game_state.board[5][0].color, 'X')
        self.assertEqual(new_game_state.board[5][1].color, 'X')
        self.assertEqual(new_game_state.board[5][2].color, 'X')

    def test_a_faller_can_be_created_and_appear_with_only_the_bottommost(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents([' X ', '   ', '   ', 'X X'])
        new_game_state.create_a_faller(1, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        self.assertEqual(new_game_state.faller_pos, [2,1])

    def test_jewels_can_match_after_starting_with_contents(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents([' X ', '   ', '   ', 'X X'])
        self.assertEqual(new_game_state.board[5][0].status, MATCH)
        self.assertEqual(new_game_state.board[5][1].status, MATCH)
        self.assertEqual(new_game_state.board[5][2].status, MATCH)

    def test_matched_jewels_can_disappear(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents([' X ', '   ', '   ', 'X X'])
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][0], None)
        self.assertEqual(new_game_state.board[5][1], None)
        self.assertEqual(new_game_state.board[5][2], None)

    def test_jewels_fall_after_jewels_disappear(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents([' Y ', ' X ', '   ', 'X X'])
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][0], None)
        self.assertEqual(new_game_state.board[5][1].color, 'Y')
        self.assertEqual(new_game_state.board[5][2], None)

    def test_faller_can_go_down_after_one_tick(self):
        new_game_state = GameState(4, 3)
        new_game_state.create_a_faller(1, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        self.assertEqual(new_game_state.faller_pos, [3,1])

    def test_faller_can_land_when_it_cannot_be_moved_down_any_further(self):
        new_game_state = GameState(4, 3)
        new_game_state.create_a_faller(1, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][1].status, LANDED)
        self.assertEqual(new_game_state.board[4][1].status, LANDED)
        self.assertEqual(new_game_state.board[3][1].status, LANDED)

    def test_faller_freeze_at_next_tick_after_landed(self):
        new_game_state = GameState(4, 3)
        new_game_state.create_a_faller(1, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][1].status, FROZEN)
        self.assertEqual(new_game_state.board[4][1].status, FROZEN)
        self.assertEqual(new_game_state.board[3][1].status, FROZEN)

    def test_faller_can_move_left_or_right_when_possible_even_landed(self):
        new_game_state = GameState(4, 3)
        new_game_state.create_a_faller(1, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        new_game_state.move_left()
        self.assertEqual(new_game_state.faller_pos, [2,0])
        new_game_state.move_right()
        self.assertEqual(new_game_state.faller_pos, [2,1])
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.move_left()
        self.assertEqual(new_game_state.faller_pos, [5,0])
        new_game_state.move_right()
        self.assertEqual(new_game_state.faller_pos, [5,1])
        
    def test_faller_cannot_move_left_or_right_when_something_blocks(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['X Y', 'Y X', 'X Y', 'Y X'])
        new_game_state.create_a_faller(1, [Gem('S', FALLER),Gem('V', FALLER), Gem('W', FALLER)])
        new_game_state.move_left()
        self.assertEqual(new_game_state.faller_pos, [2,1])
        new_game_state.move_right()
        self.assertEqual(new_game_state.faller_pos, [2,1])

    def test_faller_can_rotate_when_possible_even_landed(self):
        new_game_state = GameState(4, 3)
        new_game_state.create_a_faller(1, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Z', FALLER)])
        new_game_state.rotate()
        self.assertEqual(new_game_state.board[new_game_state.faller_pos[0]][new_game_state.faller_pos[1]].color, 'Y')
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.rotate()
        self.assertEqual(new_game_state.board[new_game_state.faller_pos[0]][new_game_state.faller_pos[1]].color, 'X')
        
    def test_freezing_of_a_faller_postpone_by_moving_it_to_a_column_with_empty_space_underneath(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['  Y', 'Y X', 'X Y', 'Y X'])
        new_game_state.create_a_faller(0, [Gem('S', FALLER),Gem('V', FALLER), Gem('W', FALLER)])
        new_game_state.move_right()
        self.assertEqual(new_game_state.board[new_game_state.faller_pos[0]][new_game_state.faller_pos[1]].status, FALLER)
        
    def test_game_over(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['  Y', 'Y X', 'X Y', 'Y X'])
        new_game_state.create_a_faller(0, [Gem('S', FALLER),Gem('V', FALLER), Gem('W', FALLER)])
        new_game_state.one_tick()
        new_game_state.one_tick()
        self.assertEqual(new_game_state.game_over, True)

    def test_mathcing_can_be_performed_vertically(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['   ', '   ', '   ', '  Y'])
        new_game_state.create_a_faller(2, [Gem('S', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][2].status, MATCH)
        self.assertEqual(new_game_state.board[4][2].status, MATCH)
        self.assertEqual(new_game_state.board[3][2].status, MATCH)
        
    def test_mathcing_can_be_performed_horizontally(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['   ', '   ', '   ', 'Y Y'])
        new_game_state.create_a_faller(1, [Gem('S', FALLER),Gem('V', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][0].status, MATCH)
        self.assertEqual(new_game_state.board[5][1].status, MATCH)
        self.assertEqual(new_game_state.board[5][2].status, MATCH)

    def test_mathcing_can_be_performed_diagonally(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['   ', 'Y  ', 'X  ', 'SSY'])
        new_game_state.create_a_faller(1, [Gem('S', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][2].status, MATCH)
        self.assertEqual(new_game_state.board[4][1].status, MATCH)
        self.assertEqual(new_game_state.board[3][0].status, MATCH)

    def test_mathcing_sequences_longer_than_three_jewels(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['   ', '   ', '   ', '  Y'])
        new_game_state.create_a_faller(2, [Gem('Y', FALLER),Gem('Y', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        new_game_state.one_tick()
        new_game_state.one_tick()
        self.assertEqual(new_game_state.board[5][2].status, MATCH)
        self.assertEqual(new_game_state.board[4][2].status, MATCH)
        self.assertEqual(new_game_state.board[3][2].status, MATCH)
        self.assertEqual(new_game_state.board[2][2].status, MATCH)

    def test_handle_more_than_one_match_sequence(self):
        new_game_state = GameState(4, 3)
        new_game_state.create_a_faller(0, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Z', FALLER)])
        for i in range(4):
            new_game_state.one_tick()
        new_game_state.create_a_faller(1, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Z', FALLER)])
        for i in range(4):
            new_game_state.one_tick()
        new_game_state.create_a_faller(2, [Gem('X', FALLER),Gem('Y', FALLER), Gem('Z', FALLER)])
        for i in range(4):
            new_game_state.one_tick()
        for i in range(3, 6):
            for j in range(3):   
                self.assertEqual(new_game_state.board[i][j].status, MATCH)
        
    def test_the_ending_of_a_game_postpone_when_mathc_appear(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['   ', 'Y  ', 'Y  ', 'SSY'])
        new_game_state.create_a_faller(0, [Gem('X', FALLER),Gem('Z', FALLER), Gem('Y', FALLER)])
        new_game_state.one_tick()
        self.assertEqual(new_game_state.game_over, False)

    def test_faller_created_is_not_fit_game_over(self):
        new_game_state = GameState(4, 3)
        new_game_state.fill_with_contents(['Y  ', 'Y  ', 'Y  ', 'SSY'])
        new_game_state.create_a_faller(0, [Gem('X', FALLER),Gem('Z', FALLER), Gem('Y', FALLER)])
        self.assertEqual(new_game_state.game_over, True)
        
if __name__ == '__main__':
    unittest.main()
