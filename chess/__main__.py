import sys
from chess.model.game import Game

if __name__ == "__main__":
    game: Game = Game()
    if len(sys.argv) > 1:
        # print(game.board)
        debug: bool = True if sys.argv[1] == "1" else False
        game.run(debug=debug)
    else:
        game.run()
