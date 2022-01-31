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
#   --show-answer         Show the answer (for testing purposes)
````

### Simple Bot:
The answer must be given, and the bot solves in hard mode.
````
python wordle_bot.py [-h] [--allowed-words ALLOWED_WORDS] answer
#
# positional arguments:
#   answer                Provide the answer
#
# options:
#   -h, --help            show this help message and exit
#   -a ALLOWED_WORDS, --allowed-words ALLOWED_WORDS
#                         Path to text file containing list of allowed words (one word per line)
````

## TODO
Bot needs work on not guessing letters that have been discovered as "in word but wrong spot"