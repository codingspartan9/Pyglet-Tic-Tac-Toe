import time
from copy import deepcopy
from math import floor

from pyglet_utils import *
from important_variables import *


class Game:
    # The padding between the board element (circle or X) and the board
    square_right_padding = 35
    square_bottom_padding = 35
    square_left_padding = 15
    square_top_padding = 15

    # Alterable numbers
    board_line_length = 15
    board_padding = 40  # Padding between the board and the screen
    circle_outline_length = 15

    # Miscellaneous
    X = 1
    CIRCLE = -1
    EMPTY = 0
    is_player1_turn = True
    squares = []
    board = []
    game_is_done = False
    player1_color = [0, 0, 255]
    player2_color = [255, 0, 0]
    moves_left = 9
    square_length = (screen_length - board_line_length * 2) / 3
    square_height = (screen_height - board_line_length * 2) / 3
    dummy_draw_victory_line_function = lambda unused: 0  # Doesn't do anything- the default function if nothing should be drawn
    game_is_paused = False

    def draw_row_victory_line(self, index):
        offset = (self.square_height + self.board_line_length) * index
        draw_line(0, screen_length, offset + self.square_height / 2, offset + self.square_height / 2, self.victory_line_color, 15)

    def draw_column_victory_line(self, index):
        offset = (self.square_length + self.board_line_length) * index
        draw_line(offset + self.square_length / 2, offset + self.square_length / 2, 0, screen_height, self.victory_line_color, 15)

    def draw_diagonal_victory_line(self, index):
        start_left_edge, end_left_edge = 0, screen_length
        start_top_edge, end_top_edge = [0, screen_height] if index == 0 else [screen_height, 0]
        draw_line(start_left_edge, end_left_edge, start_top_edge, end_top_edge, self.victory_line_color, 15)

    def get_all_board_types(self, game_board):
        """returns: [rows, columns, diagonals]"""
        return [game_board[0] + game_board[1] + game_board[2],
                [game_board[i][j] for j in range(3) for i in range(3)],
                [game_board[i][i] for i in range(3)] + [game_board[i][2 - i] for i in range(3)]]

    @property
    def victory_line_color(self):
        return self.player1_color if self.is_player1_turn else self.player2_color