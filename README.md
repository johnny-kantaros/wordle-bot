# Wordle-bot


## Introduction

New York Times's "Wordle" has gone viral this year. If you are not familiar, check out the official website here:

https://www.nytimes.com/games/wordle/index.html

Like many, I try to solve the Wordle each morning (if you are not familiar with the rules, click [here](#rules)). Recently, I decided to create an algorithm that could solve the Wordle as efficiently as possible. 


## Methodology

* This is a high level summary. For more detail, see the source code (wordle-bot.py)

For this project, I developed a ranking algorithm which maximized the likelihood of finding Yellow/Green letters (and concurrently narrowed down the list most optimally).

While Wordle recognizes for over 12k valid 5-letter guesses, only a small subset (~2k) will serve as possible answers. Therefore, my first step was reading in both of these lists into my program. I chose dictionaries to be the proper data structure for this project, as each word will have a corresponding weight (created in a later step). Having two separate dicts (one for possible guess / one for possible answers) is very important, as it allows me to keep track of remaining answers while concurrently analyzing top guesses to narrow down the list.

After reading in the lists, we will start the game. For each round of the game, we will perform the following metrics on the remaining word list:

1. Loop through each possible answer and keep track of both letter location (where letter appears in word) and letter distribution (how frequently certain    letters occur)

2. Calculate "Weights" for each word by summing Z-Scores's of letter location and letter distribution. NOTE: double letters will be penalized.

3. Sort lists in descending order (best guess at top of list)


I also added a 'Filler' functionality to this version of my Wordle bot. Filler words can be very useful when you only have a few guesses left, yet many words with very similar structures.

For example, the ending -ATCH is very common in 5-Letter words. If you guessed "MATCH" in the first round and received the following results,

X G G G G 

then you would have 6 guesses left:

LATCH
BATCH
PATCH
WATCH
CATCH
HATCH

A helpful filler word might be "BLOWN" which narrows down BATCH, LATCH, and WATCH

Consequently, although filler words don't offer a valid "winning word," they can be helpful in these select scenarios.


## Technologies

Python 3.10.6


## Rules

See the following link for a helpful guide:

https://www.wikihow.com/Play-Wordle



