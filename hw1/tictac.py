from itertools import chain


class bcolors:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    CYMAN = '\033[96m'
    ENDC = '\033[0m'


TIC_COLOR, TAC_COLOR = bcolors.RED, bcolors.GREEN
ROUND_COLOR, DRAW_COLOR = bcolors.YELLOW, bcolors.PURPLE
ERROR_COLOR = bcolors.CYMAN
TIC = f'{TIC_COLOR}X{bcolors.ENDC}'
TAC = f'{TAC_COLOR}O{bcolors.ENDC}'


class TicTacGame():

    def _get_available(self):
        return [str(el) for el in self.board if isinstance(el, int)]

    def show_board(self):
        print('-'*13)
        for i in range(3):
            print('| {} | {} | {} |'.format(*[self.board[shft + 3*i]
                  for shft in range(3)]))
            print('-'*13)

    def validate_input(self, player_num):
        tictac = TIC if player_num == 0 else TAC
        available = self._get_available()
        while True:
            print(f'Player{player_num}, please enter the place for "{tictac}"')
            print(f'Available places are: {bcolors.GREEN}'
                  f'{", ".join(available)}{bcolors.ENDC}')
            print()
            self.show_board()
            try:
                place = input()
                if not (place in available):
                    raise ValueError
                place = int(place)
            except ValueError:
                self._cool_print(f" Place '{place}' is not available, please "
                                 "try again! ", ch='!', color=ERROR_COLOR)
            else:
                self.board[place] = tictac
                return

    def start_game(self):
        self.board = [i for i in range(9)]
        round_num = 0
        while self.check_winner() and len(self._get_available()) != 0:
            self._cool_print(f' ROUND {round_num}... FIGHT! ',
                             ch=f'{round_num}', color=ROUND_COLOR)
            self.validate_input(player_num=round_num % 2)
            round_num += 1
        self.show_board()

    def _cool_print(self, s, ch='*', color=None):
        cs = color if color is not None else ''
        cool_s = '\n'.join([f'{cs}{ch}'*(len(s)+2), f'{ch}{s}{ch}',
                            f'{ch}'*(len(s)+2), bcolors.ENDC])
        print(cool_s)

    def check_winner(self):
        # row check
        gen_row = ([self.board[shft+i*3] for shft in range(3)]
                   for i in range(3))
        gen_col = (self.board[i::3] for i in range(3))
        gen_diags = (_ for _ in [self.board[::4], self.board[2:7:2]])
        # diag check
        for a, b, c in chain(gen_row, gen_col, gen_diags):
            if a == b == c:
                player_num = 0 if a == TIC else 1
                self._cool_print(f' Player{player_num} won! Congrats! ', ch=a)
                return False
        if len(self._get_available()) == 0:
            self._cool_print(' DRAW! ', ch='~', color=DRAW_COLOR)
            return False
        return True


if __name__ == '__main__':
    game = TicTacGame()
    game.start_game()
