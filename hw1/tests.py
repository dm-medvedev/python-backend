import unittest
from io import StringIO
from unittest.mock import patch

from tictac import TAC, TIC, TicTacGame


class TestTicTacGame(unittest.TestCase):
    def setUp(self):
        self.game = TicTacGame()
        self.game.board = [i for i in range(9)]

    def test_show_board1(self):
        with self.assertRaises(AttributeError):
            TicTacGame().show_board()

    def test_show_board2(self):
        true_output = "-------------\n| 0 | 1 | 2 |\n" + \
                      "-------------\n| 3 | 4 | 5 |\n" + \
                      "-------------\n| 6 | 7 | 8 |\n" + \
                      "-------------\n"
        with patch('sys.stdout', new=StringIO()) as output:
            self.game.show_board()
            self.assertEqual(output.getvalue(), true_output)

    def test_validate_input1(self):
        with self.assertRaises(AttributeError):
            TicTacGame().test_validate_input()

    def test_validate_input2(self):
        incor = 'incorrect input'

        def my_input():
            if my_input.cnt < 1:
                my_input.cnt += 1
                return incor
            else:
                raise Exception("Test Exception")

        my_input.cnt = 0
        with patch('sys.stdout', new=StringIO()) as output,\
             patch('builtins.input', new=my_input):
            board_before = self.game.board.copy()
            try:
                self.game.validate_input(0)
            except Exception as e:
                if str(e) != 'Test Exception':
                    raise e
            self.assertEqual(board_before, self.game.board)
            self.assertTrue(f" Place '{incor}' is not available" +
                            ", please try again! " in output.getvalue())

    def test_validate_input3(self):
        def my_input():
            res = None
            if my_input.cnt < 2:
                res = '4'
            elif my_input.cnt == 2:
                res = '3'
            my_input.cnt += 1
            return res

        my_input.cnt = 0
        with patch('sys.stdout', new=StringIO()) as output,\
             patch('builtins.input', new=my_input):
            true_board = self.game.board.copy()
            true_board[4] = TIC
            self.game.validate_input(0)
            self.assertEqual(true_board, self.game.board)
            self.assertTrue(f'Player0, please enter the place for "{TIC}"'
                            in output.getvalue())
            true_board[3] = TAC
            self.game.validate_input(1)
            self.assertEqual(true_board, self.game.board)
            self.assertTrue(f'Player1, please enter the place for "{TAC}"'
                            in output.getvalue())
            self.assertTrue(" Place '4' is not available" +
                            ", please try again! " in output.getvalue())

    def test_check_winner1(self):
        with self.assertRaises(AttributeError):
            TicTacGame().check_winner()

    def test_check_winner2(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(self.game.check_winner())
            self.game.board = [TIC, 1, TAC,
                               TIC, TAC, 5,
                               TIC, 7, 8]
            self.assertFalse(self.game.check_winner())
            self.assertTrue('Player0 won! Congrats!'
                            in output.getvalue())

    def test_check_winner3(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(self.game.check_winner())
            self.game.board = [TAC, TIC, TAC,
                               TIC, TAC, TIC,
                               6, TIC, TAC]
            self.assertFalse(self.game.check_winner())
            self.assertTrue('Player1 won! Congrats!'
                            in output.getvalue())

    def test_check_winner4(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(self.game.check_winner())
            self.game.board = [TAC, TIC, TAC,
                               TIC, TAC, TIC,
                               TIC, TAC, TIC]
            self.assertFalse(self.game.check_winner())
            self.assertTrue('DRAW!' in output.getvalue())

    def test_start_game1(self):
        gen = (_ for _ in ['0', '1', '3', '4', '6'])

        def my_input():
            return next(gen)

        with patch('sys.stdout', new=StringIO()) as output,\
             patch('builtins.input', new=my_input):
            self.game.start_game()
            self.assertTrue('Player0 won! Congrats!'
                            in output.getvalue())


if __name__ == '__main__':
    unittest.main()
