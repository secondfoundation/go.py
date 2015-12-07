from random import randint

class Random_AI:
    def get_move(self, board):
        # ignore the board and make a random move
        x = randint(0, board.size - 1)
        y = randint(0, board.size - 1)
        return x, y
