# wordle_bot.py - Bot to solve Wordle. The answer must be given, and the bot solves in hard mode.

# Usage: wordle_bot.py [-h] [--allowed-words ALLOWED_WORDS] answer
#
# positional arguments:
#   answer                Provide the answer
#
# options:
#   -h, --help            show this help message and exit
#   -a ALLOWED_WORDS, --allowed-words ALLOWED_WORDS
#                         Path to text file containing list of allowed words (one word per line)

import argparse
import re
from collections import Counter
from string import ascii_lowercase

from wordle import check_guess, get_word_list, print_progress


def get_letter_scores(words_file):
    with open(words_file) as f:
        letter_scores_raw = Counter(
            letter for line in f for letter in line.lower() if letter in ascii_lowercase
        )

    least_common_letter = min(letter_scores_raw, key=letter_scores_raw.get)
    lowest_score = letter_scores_raw[least_common_letter]
    most_common_letter = max(letter_scores_raw, key=letter_scores_raw.get)
    highest_score = letter_scores_raw[most_common_letter]

    def normalize_score(score):
        # Highest score is 20, lowest is 0
        return (
            score[0],
            20 * (score[1] - lowest_score) / (highest_score - lowest_score),
        )

    letter_scores_norm = dict(map(normalize_score, letter_scores_raw.items()))

    return letter_scores_norm


def get_word_score(word, letter_scores):
    word_score = 0
    for letter in word:
        word_score = word_score + letter_scores[letter]

    return word_score


def get_best_word(
    word_list,
    must_use,
    locked,
    eliminated_letters,
    guesses,
    letter_scores,
    allow_repeat_letters=False,
):
    def meets_requirements(
        word, required_letters, regex, discarded_letters, previous_guesses
    ):
        for letter in required_letters:
            if letter not in word:
                return False

        if not re.match(regex, word):
            return False

        for letter in discarded_letters:
            if letter in word:
                return False

        if word in previous_guesses:
            return False

        return True

    if eliminated_letters:
        word_list = [
            word
            for word in word_list
            if meets_requirements(word, must_use, locked, eliminated_letters, guesses)
        ]
    print(f"Number of possibilities: {len(word_list)}")

    def contains_repeat_letters(word):
        for letter in word:
            if word.count(letter) > 1:
                return True

        return False

    if not allow_repeat_letters:
        word_list = [word for word in word_list if not contains_repeat_letters(word)]
        print(f"After removing repeats: {len(word_list)}")

    word_list_scored = dict()
    for word in word_list:
        word_list_scored[word] = get_word_score(word, letter_scores)

    best_word = max(word_list_scored, key=word_list_scored.get)
    print(f"Best word: {best_word}, Score = {word_list_scored[best_word]}")

    return best_word


def main(answer):
    arg_parser = argparse.ArgumentParser(
        description="Bot to solve Wordle. The answer must be given, and the bot solves in hard mode."
    )
    arg_parser.add_argument("answer", action="store", help="Provide the answer")
    arg_parser.add_argument(
        "-a",
        "--allowed-words",
        action="store",
        help="Path to text file containing list of allowed words (one word per line)",
        default="words_alpha.txt",
    )
    args = arg_parser.parse_args()
    answer = vars(args)["answer"]
    words_file = vars(args)["allowed_words"]

    letter_scores = get_letter_scores(words_file)
    word_list = get_word_list(words_file)

    if len(answer) != 5:
        raise Exception("Answer must be a 5 letter word.")
    if answer not in word_list:
        raise Exception("Answer not in word list.")
    else:
        print(f"Answer: {answer}")

    guesses, keys, results, eliminated_letters, must_use, locked = (
        [],
        [],
        [],
        set(),
        set(),
        "",
    )

    for num_guess in range(1, 7):
        print(f"\nGuess {num_guess}")

        if num_guess <= 2:
            allow_repeats = False
        else:
            allow_repeats = True
        best_word = get_best_word(
            word_list,
            must_use,
            locked,
            eliminated_letters,
            guesses,
            letter_scores,
            allow_repeat_letters=allow_repeats,
        )
        guesses.append(best_word)

        key, result, eliminated_letters, must_use, locked = check_guess(
            hard_mode=True,
            guess=best_word,
            answer=answer,
            absent_letters=eliminated_letters,
            must_use=must_use,
        )
        keys.append(key)
        results.append(result)

        if key == "11111":
            print_progress(guesses, keys, results, eliminated_letters, success=True)
            print("\nSuccess!")
            break
        else:
            print_progress(guesses, keys, results, eliminated_letters, success=False)

    if key != "11111":
        print("\nFailure!")


if __name__ == "__main__":
    main("tests")