# wordle_bot.py - Bot to solve Wordle. The answer must be given, and the bot solves in hard mode.

# Usage: wordle_bot.py [-h] [--allowed-words ALLOWED_WORDS] answer
#
# options:
#   -h, --help            show this help message and exit
#   -a ANSWER, --answer ANSWER
#                         Provide the answer
#   -w ALLOWED_WORDS, --allowed-words ALLOWED_WORDS
#                         Path to text file containing list of allowed words (one word per line)
#   -v, --verbose         Display additional outputs

import argparse
import re
from collections import Counter
from string import ascii_lowercase

from wordle import check_guess, get_progress, get_word_list


def get_letter_scores(word_list, verbose=True):
    letter_scores_raw = Counter(
        letter for word in word_list for letter in word if letter in ascii_lowercase
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
    if verbose:
        print(f"Letter scores: {letter_scores_norm}")

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
    spot_reqs,
    eliminated_letters,
    guesses,
    allow_repeat_letters=False,
    verbose=True,
):
    def meets_requirements(word):
        for spot, letter in enumerate(word):
            if letter in spot_reqs[spot + 1]:
                return False

        for letter in must_use:
            if letter not in word:
                return False

        if not re.match(locked, word):
            return False

        for letter in eliminated_letters:
            if letter in word:
                return False

        if word in guesses:
            return False

        return True

    if eliminated_letters:
        word_list = [word for word in word_list if meets_requirements(word)]
    if verbose:
        print(f"Number of possibilities: {len(word_list)}")

    def contains_repeat_letters(word):
        for letter in word:
            if word.count(letter) > 1:
                return True

        return False

    if not allow_repeat_letters:
        word_list = [word for word in word_list if not contains_repeat_letters(word)]
        if verbose:
            print(f"After removing repeats: {len(word_list)}")

    if len(word_list) == 1:
        best_word = word_list[0]
        if verbose:
            print(f"Only remaining word: {best_word}")
    else:
        letter_scores = get_letter_scores(word_list, verbose)
        word_list_scored = dict()
        for word in word_list:
            word_list_scored[word] = get_word_score(word, letter_scores)

        best_word = max(word_list_scored, key=word_list_scored.get)
        if verbose:
            print(f"Best word: {best_word}  | Score = {word_list_scored[best_word]}")

    return best_word


def get_answer_key(guess, absent_letters, must_use):
    while True:
        answer_key_string = input("Submit Answer Key:")
        if re.match(r"^[-01]{5}$", answer_key_string):
            break
        else:
            print("INVALID ANSWER KEY. Try again.")

    answer_key, result, locked = dict(), [], []
    for spot, char in enumerate(answer_key_string):
        answer_key[spot + 1] = char

    for spot, letter in enumerate(guess):
        if answer_key[spot + 1] == "1":
            result.append(letter.upper())
            must_use.add(letter)
            locked.append(letter)
        elif answer_key[spot + 1] == "0":
            result.append(letter.lower())
            must_use.add(letter)
            locked.append(".")
        else:
            result.append("-")
            locked.append(".")
            if letter not in must_use:
                absent_letters.add(letter)

    result_string = "".join(result)
    locked_string = "".join(locked)

    return answer_key, result_string, absent_letters, must_use, locked_string


def get_spot_requirements(spot_reqs, guess, answer_key):
    for spot, not_in_spot in spot_reqs.items():
        letter = guess[spot - 1]
        code = answer_key[spot]
        if code == "-" or code == "0":
            not_in_spot.add(letter)

    return spot_reqs


def main():
    arg_parser = argparse.ArgumentParser(
        description="Bot to solve Wordle. The answer must be given, and the bot solves in hard mode."
    )
    arg_parser.add_argument("-a", "--answer", action="store", help="Provide the answer")
    arg_parser.add_argument(
        "-w",
        "--allowed-words",
        action="store",
        help="Path to text file containing list of allowed words (one word per line)",
        default="words_wordle.txt",
    )
    arg_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Display additional outputs"
    )
    args = arg_parser.parse_args()
    answer = vars(args)["answer"]
    words_file = vars(args)["allowed_words"]
    verbose = vars(args)["verbose"]

    word_list = get_word_list(words_file)

    if answer:
        answer = answer.lower()
        if len(answer) != 5:
            raise Exception("Answer must be a 5 letter word.")
        if answer not in word_list:
            raise Exception("Answer not in word list.")
        else:
            print(f"Answer: {answer.upper()}")
    else:
        print("No answer provided. Play-along mode enabled.")
        print("User must provide answer key as a single string after each guess.")
        print('"-" if the letter is not in the word in any spot (gray)')
        print('"0" if the letter is in the word but in the wrong spot (yellow/blue)')
        print('"1" if the letter is in the word and in the correct spot (green/orange)')
        print('eg. "-0-10"')

    guesses, answer_keys, results, eliminated_letters, must_use, locked, spot_reqs = (
        [],
        [],
        [],
        set(),
        set(),
        "",
        dict(),
    )
    for spot in range(1, 6):
        spot_reqs[spot] = set()

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
            spot_reqs,
            eliminated_letters,
            guesses,
            allow_repeat_letters=allow_repeats,
            verbose=verbose,
        )
        guesses.append(best_word)

        if answer:
            answer_key, result, eliminated_letters, must_use, locked = check_guess(
                hard_mode=True,
                guess=best_word,
                answer=answer,
                absent_letters=eliminated_letters,
                must_use=must_use,
            )
        else:
            print(f"Optimal Guess: {best_word.upper()}")
            answer_key, result, eliminated_letters, must_use, locked = get_answer_key(
                guess=best_word, absent_letters=eliminated_letters, must_use=must_use
            )

        answer_keys.append(answer_key)
        results.append(result)

        spot_reqs = get_spot_requirements(spot_reqs, best_word, answer_key)

        success = get_progress(
            guesses,
            answer_keys,
            results,
            eliminated_letters,
            must_use,
            locked,
            hard_mode=True,
        )

        if success:
            break
        else:
            if verbose:
                print(f"Spot Requirements: {spot_reqs}")

    if not success:
        print("\nFailure!")


if __name__ == "__main__":
    main()
