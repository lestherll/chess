from unittest import TestCase

from chess.custom_typehints import Colour, GameStatus
from chess.model.board import Board
from chess.model.game import GameState
from chess.model.player import Player


class TestGameState(TestCase):

    def test_game_state_player_init(self):
        game_state: GameState = GameState(Board(), Player("1", Colour.BLACK), Player("2", Colour.WHITE))

        self.assertTupleEqual((Player("1", Colour.BLACK), Player("2", Colour.WHITE)),
                              (game_state.black_player, game_state.white_player))
        self.assertFalse(game_state.turn_number)
        self.assertFalse(game_state.moves_made)
        self.assertIs(GameStatus.NORMAL, game_state.status)
