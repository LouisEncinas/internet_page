from time import sleep
from chess import *
import random

def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def mainloop():
    c = Chess()
    ipt = ''
    while ipt != 'STOP':
        clear()
        print('')
        c.show()
        print('')
        for move in c._possible_moves():
            print(move)
        print('')
        ipt = input('Next move : ')
        if ipt != 'STOP':
            _from,to = tuple(ipt.split(' '))
            c.move(_from, to)

def random_game():
    random.seed()

    c = Chess()
    lst_moves = c._possible_moves()
    while lst_moves:
        # clear()
        print('')
        c.show()
        print('')
        sleep(0.5)
        lst_moves = c._possible_moves()
        move = lst_moves[random.randint(0, len(lst_moves)-1)]
        c.move(move._from, move.to)
        lst_moves = c._possible_moves()


def main():
    mainloop()

if __name__ == "__main__":
    main()