# wordle.py - Play Wordle in the command line

# Usage: wordle.py [-h] [--hard] [--answer ANSWER] [--show-answer]
#
# options:
#   -h, --help            show this help message and exit
#   --hard                Enable hard mode
#   -a ANSWER, --answer ANSWER
#                         Provide the answer
#   --show-answer         Show the answer (for testing purposes)
#   -w ALLOWED_WORDS, --allowed-words ALLOWED_WORDS
#                         Path to text file containing list of allowed words (one word per line)

# Output key:
# Turn : guess | symbolic result | alphabet result
# - : letter not in word in any spot
# 0 : letter in word, but in the wrong spot (shown as lower case letter)
# 1 : letter in the word, and in the correct spot (shown as upper case letter)

import argparse
import random
import re


def get_word_list(word_list_file="words_wordle.txt"):
    # Read word list and return only 5-letter words
    with open(word_list_file, "r") as w:
        words = w.read().splitlines()
        five_letter_words = [word.lower() for word in words if len(word) == 5]

        return five_letter_words


def get_guess(hard_mode, num_guess, five_letter_words, must_use, locked):
    if not hard_mode:
        locked = r"^[A-Za-z]{5}$"  # Any 5-letter word

    satisfied = False
    while not satisfied:
        guess = input(f"\nEnter Guess {num_guess}: ").lower()
        satisfied = True

        if len(guess) != 5:
            print("Guess must be a 5 letter word. Try again.")
            satisfied = False
        elif guess not in five_letter_words:
            print("Guess must be in word list. Try again.")
            satisfied = False

        if not re.match(locked, guess):
            print(
                "HARD MODE: Any revealed hints must be used in subsequent guesses. Try again."
            )
            print(f"HARD MODE: Guess must match the RegEx: {locked}")
            satisfied = False
            continue

        for letter in must_use:
            if letter not in guess:
                print(
                    "HARD MODE: Any revealed hints must be used in subsequent guesses. Try again."
                )
                print(f'HARD MODE: Guess must include "{letter}".')
                satisfied = False

    return guess


def check_guess(hard_mode, guess, answer, absent_letters, must_use):
    answer_key, result, locked = dict(), [], []
    remaining = list(answer)
    for spot, letter in enumerate(guess):
        if letter == answer[spot]:
            answer_key[spot + 1] = "1"
            result.append(letter.upper())
            remaining[spot] = ""
            if hard_mode:
                must_use.add(letter)
                locked.append(letter)
        elif letter in remaining:
            answer_key[spot + 1] = "0"
            result.append(letter)
            if hard_mode:
                must_use.add(letter)
                locked.append(".")
        else:
            answer_key[spot + 1] = "-"
            result.append("-")
            if letter not in must_use:
                absent_letters.add(letter)
            if hard_mode:
                locked.append(".")

    result_string = "".join(result)
    locked_string = "".join(locked)

    return answer_key, result_string, absent_letters, must_use, locked_string


def print_progress(guesses, answer_keys, results, eliminated_letters):
    for num_guess, guess in enumerate(guesses):
        answer_key_string = "".join(answer_keys[num_guess].values())
        print(
            " | ".join(
                [str(num_guess + 1), guess, answer_key_string, results[num_guess]]
            )
        )

    if answer_key_string == "11111":
        success = True
        print("\nSuccess!")
    else:
        success = False
        print(f"Eliminated letters: {eliminated_letters}")

    return success


def main():
    arg_parser = argparse.ArgumentParser(description="Play Wordle in the command line")
    arg_parser.add_argument("--hard", action="store_true", help="Enable hard mode")
    arg_parser.add_argument("-a", "--answer", action="store", help="Provide the answer")
    arg_parser.add_argument(
        "-w",
        "--allowed-words",
        action="store",
        help="Path to text file containing list of allowed words (one word per line)",
        default="words_wordle.txt",
    )
    arg_parser.add_argument(
        "-v",
        "--show-answer",
        action="store_true",
        help="Show the answer (for testing purposes)",
    )
    args = arg_parser.parse_args()
    hard_mode = vars(args)["hard"]
    answer = vars(args)["answer"]
    show_answer = vars(args)["show_answer"]

    if hard_mode:
        print(f"Game mode: HARD")
    else:
        print(f"Game mode: EASY")

    five_letter_words = get_word_list("words_wordle.txt")

    if answer:
        if len(answer) != 5:
            raise Exception("Answer must be a 5 letter word.")
        if answer not in five_letter_words:
            raise Exception("Answer not in word list.")
        else:
            if show_answer:
                print(f"Given answer: {answer}")
    else:
        answer = random.choice(five_letter_words)
        if show_answer:
            print(f"Random answer: {answer}")

    guesses, answer_keys, results, eliminated_letters, must_use, locked = (
        [],
        [],
        [],
        set(),
        set(),
        "",
    )
    for num_guess in range(1, 7):
        guess = get_guess(hard_mode, num_guess, five_letter_words, must_use, locked)
        guesses.append(guess)

        key, result, eliminated_letters, must_use, locked = check_guess(
            hard_mode, guess, answer, eliminated_letters, must_use
        )
        answer_keys.append(key)
        results.append(result)

        success = print_progress(guesses, answer_keys, results, eliminated_letters)
        if success:
            break

    if not success:
        print("\nFailure!")


if __name__ == "__main__":
    main()
