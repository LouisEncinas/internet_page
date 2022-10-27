from time import sleep
from chess import *
import random

def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def mainloop():
    c = Chess()
    ipt = ''
    while ipt != 'STOP' and not c.check_mate:
        clear()
        print('')
        c.show()
        print('')
        # print(c.check, c.check_mate)
        # print('')
        # print(c.moves)
        # print('')
        # for move in c.psb_mv:
        #     print(move)
        # print('')
        ipt = input('Next move : ')
        if ipt != 'STOP':
            _from,to = tuple(ipt.split(' '))
            c.move(_from, to)
    if c.check_mate:
        clear()
        c.show()

def random_game():
    random.seed()

    c = Chess()
    lst_moves = c._possible_moves()
    move = None
    while lst_moves:
        clear()
        print('')
        c.show()
        print('')
        if move is not None: print(move)
        input()
        move = c.psb_mv[random.randint(0, len(c.psb_mv)-1)]
        c.move(move._from, move.to)

def main():
    random_game()

if __name__ == "__main__":
    main()