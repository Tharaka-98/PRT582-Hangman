"""
Hangman Game Module

A Python implementation of the classic Hangman word guessing game.
Features include multiple difficulty levels, visual hangman drawings,
and support for both single words and phrases.
"""

import time
import random
from wordslist import phrases, words


# Function to display the hangman drawing
def draw_hangman(incorrect):
    """
    Draws the hangman state based on the number of incorrect guesses.
    """
    hangman_states = [
        ''' ________
|        |
|        O
|
|
|
|__       ''',
        ''' ________
|        |
|        O
|        |
|
|
|__       ''',
        ''' ________
|        |
|        O
|       /|
|
|
|__       ''',
        ''' ________
|        |
|        O
|       /|\\
|
|
|__       ''',
        ''' ________
|        |
|        O
|       /|\\
|        |
|
|__       ''',
        ''' ________
|        |
|        O
|       /|\\
|        |
|       /
|__        ''',
        ''' ________
|        |
|        O
|       /|\\
|        |
|       / \\
|__       '''
    ]
    # Ensure 'incorrect' is within the valid range
    incorrect = max(0, min(incorrect, 6))  # clamp to [0, 6]
    print(hangman_states[incorrect])


# Function to display the current hint
def display_hint(word):
    """
    Displays the word with guessed letters filled in (spaces preserved).
    """
    print(" ".join(word))  # Join the hint letters with a space and print


# handle countdown
def timer(sec):
    """
    Displays the countdown timer in minutes:seconds format.
    """
    while sec:
        mins, sec = divmod(sec, 60)
        # Fixed the formatting
        time_left = f"{mins:02}:{sec:02}"
        print(f"Time left: {time_left}", end="\r")
        time.sleep(1)
        sec -= 1


# update the word state
def update_word_state(word, guessing_word, guess):
    """
    Updates the word with correctly guessed letters.
    """
    correct = 0
    for i, char in enumerate(guessing_word):
        if char == guess:
            word[i] = guess
            correct += 1
    return correct


# check if the guess is valid
def is_valid_guess(guess, guessed_letters):
    """
    Checks if the guess is a valid, single alphabetic character and hasn't been
    guessed already.
    """
    if len(guess) != 1 or not guess.isalpha():
        print("Invalid numerical or special character Input")
        return False
    if guess in guessed_letters:
        print(f"You've already guessed '{guess}'. Try a different letter.")
        return False
    return True


def level_selection():
    """
    Prompts the user to select a difficulty level and returns the corresponding
    word list.
    """
    print("Welcome to Hangman!")
    print("Select your desired level:")
    print("1. Short Words")
    print("2. Phrases")

    level = input("Enter your level number: ")
    if level == "1":
        return words
    if level == "2":
        return phrases
    return words


def hangman_game():
    """
    Main game loop to run Hangman with level selection, guesses, and win/lose
    conditions.
    """
    # Select the difficulty level and assign to a variable
    level = level_selection()

    # Pick a random word from the list
    guessing_word = random.choice(level)

    # Create a list of underscores for the word
    word = ["_"] * len(guessing_word)

    # Ensure spaces are placed correctly in the word
    for i, char in enumerate(guessing_word):
        if char == " ":
            word[i] = " "

    incorrect = 0
    correct = 0
    lives = 6
    # sec = 15  # keep if you later wire timer(); not used now

    # To track already guessed letters (both correct and incorrect)
    guessed_letters = set()
    is_working = True

    # Game loop
    while is_working:
        # Draw hangman based on incorrect guesses
        draw_hangman(incorrect)

        # Display the current state of the word
        display_hint(word)
        print(
            f"Lives: {lives} | Guessed: "
            f"{' '.join(sorted(guessed_letters)) or '(none)'}"
        )

        # Display countdown timer before user input
        # print("You have 15 seconds to guess!")
        # timer(sec)

        # Game over due to losing
        if incorrect == 6:
            print("\nBetter luck next time!")
            print(f"The correct word was {guessing_word}")
            is_working = False
            break

        # Check for win or loss
        # remove the space in the phrase
        if correct == len(guessing_word.replace(" ", "")):
            print("\nCongratulations, you win!")
            print(f"The correct word was {guessing_word}")
            is_working = False
            break

        # Take the player's guess
        # guess = input('\nPlease guess a letter: ').lower()

        # Take the player's guess and quit command
        guess = input(
            '\nPlease guess a letter (or type "quit" to quit): '
        ).lower().strip()

        # quit command
        if guess == "quit":
            print("\nYou chose to quit. Thanks for playing!")
            print(f"The correct word was: {guessing_word}")
            is_working = False
            break

        if is_valid_guess(guess, guessed_letters):
            # Add the guess to the set of guessed letters
            guessed_letters.add(guess)

            # If the guessed letter is a space, continue without penalty
            if guess == " ":
                print("Spaces do not count as incorrect guesses. Keep going!")
                continue

            # Check if the guessed letter is in the word
            if guess in guessing_word:
                correct += update_word_state(word, guessing_word, guess)
            else:
                # Increment incorrect counter if the guess is wrong
                incorrect += 1
                lives -= 1

        print("****************")
        # Draw hangman
        draw_hangman(incorrect)
        print(f"wrong guess {incorrect}")
        print("****************")


if __name__ == "__main__":
    hangman_game()
