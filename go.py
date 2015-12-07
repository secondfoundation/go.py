#!/usr/bin/env python

import argparse
import sys

from go import Board, BoardError, View, clear, getch
from ai import Random_AI

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Starts a game of go in the terminal.')
    parser.add_argument('-s', '--size', type=int, default=19, help='size of board')
    parser.add_argument("-a", "--ai", action="store_true", help='whether to play against the AI')

    # have argument for playing again AI...
    # have method to get a move from the AI, given the current board
    # have AI play, then draw board

    args = parser.parse_args()

    if args.size < 7 or args.size > 19:
        sys.stdout.write('Board size must be between 7 and 19!\n')
        sys.exit(0)

    # Initialize board and view
    board = Board(args.size)
    view = View(board)
    ai = Random_AI()
    err = None

    # User actions
    def move():
        """
        Makes a move at the current position of the cursor for the current
        turn.
        """
        board.move(*view.cursor)
        if args.ai:
            do_ai_move()

        view.redraw()

    def do_ai_move():
        valid_move = False
        while not valid_move:
            ai_move = ai.get_move(board)
            try:
                board.move(*ai_move)
                valid_move = True
            except BoardError as be:
                print "AI made invalid move!  Moving again: " + be.message

    def undo():
        """
        Undoes the last move.
        """
        board.undo()
        view.redraw()

    def redo():
        """
        Redoes an undone move.
        """
        board.redo()
        view.redraw()

    def exit():
        """
        Exits the game.
        """
        sys.exit(0)

    # Action keymap
    KEYS = {
        'w': view.cursor_up,
        's': view.cursor_down,
        'a': view.cursor_left,
        'd': view.cursor_right,
        ' ': move,
        'u': undo,
        'r': redo,
        '\x1b': exit,
    }

    # Main loop
    while True:
        # Print board
        clear()
        sys.stdout.write('{0}\n'.format(view))
        sys.stdout.write('Black: {black} <===> White: {white}\n'.format(**board.score))
        sys.stdout.write('{0}\'s move... '.format(board.turn))

        if err:
            sys.stdout.write('\n' + err + '\n')
            err = None

        # Get action key
        c = getch()

        try:
            # Execute selected action
            KEYS[c]()
        except BoardError as be:
            # Board error (move on top of other piece, suicidal move, etc.)
            err = be.message
        except KeyError:
            # Action not found, do nothing
            pass


if __name__ == '__main__':
    main()
