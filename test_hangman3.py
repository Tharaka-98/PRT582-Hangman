import unittest
from io import StringIO
import sys
from hangman3 import draw_hangman, is_valid_guess, update_word_state, level_selection, hangman_game
from unittest.mock import patch
from wordslist import words, phrases

class TestHangman(unittest.TestCase):

    @patch('builtins.input', return_value='1')   #user input 1 for short words
    def test_level_selection_short_words(self, mock_input):
        result = level_selection()
        self.assertEqual(result, words)

    @patch('builtins.input', return_value='2') # user input 2 for phrases
    def test_level_selection_phrases(self, mock_input):
        result = level_selection()
        self.assertEqual(result, phrases)

    @patch('builtins.input', return_value='3') # user input 3 for invalid input
    def test_level_selection_invalid_input(self, mock_input):
        result = level_selection()
        self.assertEqual(result, words) # default to short words

    def test_draw_hangman(self):
        # Capture the output
        captured_output = StringIO()
        sys.stdout = captured_output
        # Test for incorrect guesses
        draw_hangman(0)
        self.assertIn("O", captured_output.getvalue())  # Should contain the hangman drawing
        captured_output.truncate(0) #clear the output
        captured_output.seek(0) #pointer at the begin of the output
        # Test for 6 incorrect guesses
        draw_hangman(6)
        self.assertIn("O", captured_output.getvalue()) # Should contain the hangman drawing
        # reset to default value
        sys.stdout = sys.__stdout__

    def test_update_word_state(self):
        word = ['_'] * 5 #Ex:- Apple
        result = update_word_state(word, 'apple', 'a')
        self.assertEqual(result, 1) #check whether updated letter replace underscore or not
        self.assertEqual(word, ['a', '_', '_', '_', '_'])

        result = update_word_state(word, 'apple', 'p')
        self.assertEqual(result, 2) #should update all the p letters in the word
        self.assertEqual(word, ['a', 'p', 'p', '_', '_'])

        result = update_word_state(word, 'apple', 'x')
        self.assertEqual(result, 0) # should not update the word
        self.assertEqual(word, ['a', 'p', 'p', '_', '_'])
        
    def test_is_valid_guess(self):
        guessed_letters = { 'a', 'b', 'c'}
        #testing for valid guess
        self.assertTrue(is_valid_guess('e', guessed_letters)) #should return valid
        #testing for invalid guess
        self.assertFalse(is_valid_guess('1', guessed_letters)) # test for numeric number and give the error message
        self.assertFalse(is_valid_guess('!', guessed_letters)) #test for special charactor and give the error message
        self.assertFalse(is_valid_guess('aa', guessed_letters)) #test for multiple letters and give the error message
        self.assertFalse(is_valid_guess('a', guessed_letters)) #test for given letter and give the error message
        self.assertFalse(is_valid_guess(' ', guessed_letters)) #test for a space

     # ---------- light integration: quit flow ----------
    @patch('builtins.input', side_effect=['1',  # level_selection -> words
                                          'quit'])  # immediately quit game
    @patch('random.choice', return_value='book')  # deterministic word
    def test_game_quit_immediately(self, _rand_choice, _input):
        # capture output to assert quit message is printed
        captured = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured

        try:
            hangman_game()
        finally:
            sys.stdout = sys_stdout_backup

        out = captured.getvalue()
        self.assertIn("You chose to quit. Thanks for playing!", out)
        self.assertIn("The correct word was:", out)
        self.assertIn("book", out)  # our mocked word

    # --- display_hint ---
    def test_display_hint_prints_board_and_spaces(self):
        from hangman3 import display_hint
        board = ['a', '_', ' ', '_']  # e.g., "a_ _" with a space in the middle
        captured = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured
        try:
            display_hint(board)
        finally:
            sys.stdout = sys_stdout_backup
        # " ".join(['a','_',' ','_']) == "a _   _"
        self.assertIn("a _   _", captured.getvalue().strip())

    # --- timer (fast) ---
    @patch("time.sleep", return_value=None)
    def test_timer_runs_without_delay_and_ticks_expected_times(self, mock_sleep):
        from hangman3 import timer
        try:
            timer(3)  # should call sleep 3 times
        except Exception as e:
            self.fail(f"timer raised unexpectedly: {e}")
        self.assertEqual(mock_sleep.call_count, 3)

    # --- hangman_game: win path ---
    @patch('builtins.input', side_effect=[
        '1',    # level_selection -> words
        'b', 'o', 'k'  # guesses for "book"
    ])
    @patch('random.choice', return_value='book')
    def test_game_win_flow(self, _rand_choice, _input):
        captured = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured
        try:
            from hangman3 import hangman_game
            hangman_game()
        finally:
            sys.stdout = sys_stdout_backup
        out = captured.getvalue()
        self.assertIn("Congratulations, you win!", out)
        self.assertIn("The correct word was book", out.replace("was ", "was "))  # tolerate punctuation/spacing

    # --- hangman_game: lose path (6 wrong) ---
    @patch('builtins.input', side_effect=[
        '1',      # level_selection -> words
        # six wrong letters for "book"
        'x', 'y', 'z', 'q', 'w', 'r'
    ])
    @patch('random.choice', return_value='book')
    def test_game_lose_flow(self, _rand_choice, _input):
        captured = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured
        try:
            from hangman3 import hangman_game
            hangman_game()
        finally:
            sys.stdout = sys_stdout_backup
        out = captured.getvalue()
        self.assertIn("Better luck next time!", out)
        self.assertIn("The correct word was book", out.replace("was ", "was "))

    # --- draw_hangman clamps to 6 ---
    def test_draw_hangman_clamps_when_incorrect_overflow(self):
        captured = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured
        try:
            draw_hangman(99)  # should show final state (legs visible)
        finally:
            sys.stdout = sys_stdout_backup
        self.assertIn("/ \\", captured.getvalue())



if __name__ == "__main__":
    unittest.main() 
        