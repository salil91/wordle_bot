# Bot to solve wordle
# Currently coding the game

# Usage: python wordle.py <game mode> <answer>
# Game modes: easy (default) / hard
# If no answer is provided, a random word is chosen.

# Output: key:
# Guess # : guess | symbolic result | alphabet result
# - : letter not in word in any spot
# 0 : letter in word, but in the wrong spot (shown as lower case letter)
# 1 : letter in the word, and in the correct spot (shown as upper case letter)

import random
import sys

import pyinputplus as pyip


def get_word_list():
    # Read word list and return only 5-letter words
    with open("words_alpha.txt", "r") as w:
        words = w.read().splitlines()
        five_letter_words = [word for word in words if len(word) == 5]

        return five_letter_words


def get_guess(game_mode, num_guess, five_letter_words, must_use, locked):
    if game_mode == "EASY":
        locked = r"^[A-Za-z]{5}$"  # Any 5-letter word

    satisfied = False
    while not satisfied:
        guess = pyip.inputChoice(
            prompt=f"\nEnter Guess {num_guess}: ",
            allowRegexes=[locked],
            choices=["cheat", "codes"],
        )
        guess = guess.lower()
        if guess not in five_letter_words:
            print("Guess must be in word list. Try again.")
            satisfied = False
        else:
            satisfied = True

        for letter in must_use:
            if letter not in guess:
                print(f'HARD MODE: Guess must include "{letter}". Try again.')
                satisfied = False

    return guess


def check_guess(game_mode, guess, answer, absent_letters, must_use):
    key, revealed, locked = [], [], []
    remaining = list(answer)
    for spot, letter in enumerate(guess):
        if letter == answer[spot]:
            key.append("1")
            revealed.append(letter.upper())
            remaining[spot] = ""
            if game_mode == "HARD":
                must_use.add(letter)
                locked.append(letter)
        elif letter in remaining:
            key.append("0")
            revealed.append(letter)
            if game_mode == "HARD":
                must_use.add(letter)
                locked.append(".")
        else:
            key.append("-")
            revealed.append("-")
            absent_letters.append(letter)
            if game_mode == "HARD":
                locked.append(".")

    key_string = "".join(key)
    revealed_string = "".join(revealed)
    locked_string = "".join(locked)

    return key_string, revealed_string, absent_letters, must_use, locked_string


def main():
    if len(sys.argv) < 2:
        game_mode = "EASY"
        prefix_game_mode = "Default "
    else:
        game_mode = sys.argv[1].upper()
        prefix_game_mode = ""

    if game_mode.upper() not in ["EASY", "HARD"]:
        print("\nUnknown game mode provided. EASY mode selected.")
        game_mode = "EASY"
    else:
        print(f"\n{prefix_game_mode}Game mode: {game_mode.upper()}")

    five_letter_words = get_word_list()

    if len(sys.argv) < 3:
        answer = random.choice(five_letter_words)
        print(f"Random answer: {answer}")
    else:
        answer = sys.argv[2].lower()
        if len(answer) != 5:
            raise Exception("Answer must be a 5 letter word.")
        if answer not in five_letter_words:
            raise Exception("Answer not in word list.")
        else:
            print(f"Given answer: {answer}")

    guesses, keys, results, eliminated_letters, must_use, locked = (
        [],
        [],
        [],
        [],
        set(),
        "",
    )
    remaining = answer
    for num_guess in range(1, 7):
        guess = get_guess(game_mode, num_guess, five_letter_words, must_use, locked)
        guesses.append(guess)
        key, result, eliminated_letters, must_use, locked = check_guess(
            game_mode, guess, answer, eliminated_letters, must_use
        )
        keys.append(key)
        results.append(result)

        for num_result, result in enumerate(keys):
            print(
                f"{num_result+1}: {guesses[num_result]} | {keys[num_result]} | {results[num_result]}"
            )

        if key == "11111":
            print("\nSuccess!\n")
            break
        else:
            print(f"Eliminated letters: {eliminated_letters}")

    if key != "11111":
        print("\nFailure!\n")


if __name__ == "__main__":
    main()
