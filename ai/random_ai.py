from random import randint

class Random_AI:
    def get_move(self, board):
        # ignore the board and make a random move
        x = randint(1, board.size)
        y = randint(1, board.size)
        return x, y
