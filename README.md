# Wordle Bot
Play Wordle in the command line, or run a bot to solve a Wordle.

## Usage
### Play Worlde:
````
python wordle.py [-h] [--hard] [--answer ANSWER] [--show-answer]
#
# options:
#   -h, --help            show this help message and exit
#   --hard                Enable hard mode
#   -a ANSWER, --answer ANSWER
#                         Provide the answer
#   -w ALLOWED_WORDS, --allowed-words ALLOWED_WORDS
#                         Path to text file containing list of allowed words (one word per line)
#   -v, --show-answer     Show the answer (for testing purposes)
````

### Simple Bot:
````
python wordle_bot.py [-h] [--allowed-words ALLOWED_WORDS] answer
#
# options:
#   -h, --help            show this help message and exit
#   -a ANSWER, --answer ANSWER
#                         Provide the answer
#   -w ALLOWED_WORDS, --allowed-words ALLOWED_WORDS
#                         Path to text file containing list of allowed words (one word per line)
#   -v, --verbose         Display additional outputs
````
If the answer is given, the bot solves it automatically in hard mode.

If the answer is not given, the user must provide the answer key as a single string after each guess.
- "-" if the letter is not in the word in any spot (gray)
- "0" if the letter is in the word but in the wrong spot (yellow/blue)
- "1" if the letter is in the word and in the correct spot (green/orange)

eg. "-0-10"


## TODO
- Improve bot to use letter scores as a function of the position which they occupy in a word.
