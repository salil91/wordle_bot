# Bot to solve wordle
# Currently coding the game

# Usage: python wordle.py <answer>
# If no answer is provided, a random word is chosen.

# Output: key:
# Guess # : guess | symbolic result | alphabet result
# _ : letter not in word in any spot
# - : letter in word, but in the wrong spot (shown as lower case letter)
# o : letter in the word, and in the correct spot (shown as upper case letter)

import random
import sys


def get_word_list():
    # Read word list and return only 5-letter words
    with open("words_alpha.txt", "r") as w:
        words = w.read().splitlines()
        five_letter_words = [word for word in words if len(word) == 5]

        return five_letter_words


def get_guess(num_guess, five_letter_words):
    # Get guess and ensure it is 5 words long and exists in the word list.
    while True:
        guess = input(f"Enter Guess {num_guess}: ").lower()
        if len(guess) != 5:
            print("Guess must be a 5 letter word.")
        elif guess not in five_letter_words:
            print("Guess must be in word list.")
        else:
            break

    return guess


def check_guess(guess, answer, absent_letters):
    key, revealed = [], []
    for spot, letter in enumerate(guess):
        if letter == answer[spot]:
            key.append("o")
            revealed.append(letter.upper())
        elif letter in answer:
            key.append("-")
            revealed.append(letter.lower())
        else:
            key.append("_")
            revealed.append("_")
            absent_letters.append(letter)

    key_string = "".join(key)
    revealed_string = "".join(revealed)

    return key_string, revealed_string, absent_letters


def main():
    five_letter_words = get_word_list()
    if len(sys.argv) < 2:
        answer = random.choice(five_letter_words)
        print(f"Random answer: {answer}")
    else:
        answer = sys.argv[1].lower()
        if len(answer) != 5:
            raise Exception("Answer must be a 5 letter word.")
        if answer not in five_letter_words:
            raise Exception("Answer not in word list.")
        else:
            print(f"Given answer: {answer}")

    guesses, keys, results, eliminated_letters = [], [], [], []
    for num_guess in range(1, 7):
        guess = get_guess(num_guess, five_letter_words)
        guesses.append(guess)
        key, result, eliminated_letters = check_guess(guess, answer, eliminated_letters)
        keys.append(key)
        results.append(result)

        for num_result, result in enumerate(keys):
            print(
                f"{num_result+1}: {guesses[num_result]} | {keys[num_result]} | {results[num_result]}"
            )

        if key == "ooooo":
            print("Success!")
            break
        else:
            print(f"Eliminated letters: {eliminated_letters}")

    if key != "ooooo":
        print("Failure!")


if __name__ == "__main__":
    main()
