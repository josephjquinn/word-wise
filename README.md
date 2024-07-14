# Word-Wise

This project is a Python implementation of a Wordle solver using the Selenium web automation framework.
Wordle is a word puzzle game where the player tries to guess a five-letter word within a limited number of attempts.

## Introduction

This repository contains a collection of Python scripts and utilities designed to simulate and analyze Wordle games,
as well as develop and test a Wordle-solving algorithm.

https://github.com/josephjquinn/word-wise/assets/81782398/4ebdb953-601d-47a7-9b9f-b12863a13923

## Selenium

In this project, we leverage the power of Selenium, a popular web automation tool, to interact with the Wordle website.
Selenium allows us to programmatically navigate the website, submit guesses, retrieve puzzle data, and gather
Wordle game statistics for analysis. Here's how Selenium is used in this project:

- #### 1. Web Scraping Results
  Selenium is employed to scrape the Wordle website and extract its html source in order to track the colors of our guesses
  It looks for the color feedback (green, yellow, white) to determine which letters are correct and in the right position,
  which are correct but in the wrong position, and which are incorrect. This is all accomplished by the `parseHTML` function in helper.py. This data is then fed to the algorithm in order to generate
  the next guess.
- #### 2. Submitting Word Guesses
  Selenium also takes charge of interacting with the Wordle website to submit guesses. It inputs each letter of the suggested guess
  into the website. Once Selenium has entered the entire guessed word, it then triggers the evaluation of the guess, and
  the process is repeated

### `game.py`

This version interacts with the Wordle game hosted on wordle-vanilla.vercel.app. This alternate version of the website
allows for unlimited games per day and the script will run for as many games as you choose.

### `solveWordScore.py`

This version will interact with the official New York Times hosted website and solve the daily wordle using my updated wordscore algorithm.

### `solveRemoval.py`

This script will solve the New Work Times worlde with my original removal algorithm that is slightly less efficeient.

## Algorithm Structure `algorithm.py`

The algorithm.py script contains a collection of functions designed to solve the puzzles and assist in generating optimal guesses.

<img width="400" src="./imgs/algorithmdiagram.png">

### Functions Overview

#### 1. `get_wordle_guesses()`

This function reads a list of potential words from the `wordlist.txt` file, serving as the pool of words from which the algorithm selects guesses during gameplay.

#### 2. `badLetters(result, guess)`

The `badLetters` function identifies and returns letters in the current guess that are marked as "w" (wrong) in the feedback result from Wordle.

#### 3. `partialLetters(result, guess)`

`partialLetters` detects letters in the guess that are marked as "y" (yellow) in the result string, indicating that they are correctly guessed but misplaced within the word.

#### 4. `correctLetters(result, guess)`

`correctLetters` identifies letters that are both correct and correctly positioned within the word. It returns the correctly placed letters marked as "g" (green) in the result string.

#### 5. `word_remover(result, guess, possible_words)`

This function refines the list of possible words based on the feedback from previous guesses. It iteratively eliminates words that contain incorrect letters, ensures the correct placement of guessed letters, and removes words with letters that have already been correctly placed.

#### 6. `letterFreq(possible_words)`

`letterFreq` calculates the frequency of each letter in each position across the list of possible words, providing insights into the distribution of letters.

#### 7. `wordScore(possible_words, frequencies)`

This function computes a score for each word in the list of possible words based on letter frequencies. It assigns higher scores to words that match the observed letter distribution and introduces a small random factor to encourage exploration.

#### 8. `bestWord(possible_words, frequencies)`

`bestWord` selects the optimal word to guess based on the computed scores. It iterates through the list of possible words and chooses the word with the lowest score, indicating the highest likelihood of matching the solution.

## Algorithm Design

The algorithm works by progressively narrowing down the list of possible words, prioritizing guesses with the highest probability of success, and ultimately solving Wordle puzzles efficiently.

<img src="./imgs/Wordbot-1.png" width="300"><img src="./imgs/Wordbot-2.png" width="300"><img src="./imgs/Wordbot-3.png" width="300">

For detailed information on each function and their implementation, refer to the `algorithm.py` script.

## Wordle Game Simulation and Testing `test.py`

This part of the project allows you to evaluate the algorithm's effectiveness in solving Wordle puzzles efficiently, it
does this by running it through a simulation of a Wordle game a set amount of times and collecting the data.

### Variable Adjustments

run_game(games): Adjust the number of Wordle games to simulate by changing the games parameter. Default is 1000

guess = "slate": Adjust this to change the starting word the simulation will use. Default is "slate"

### Example Output

```
---------------------------------
Total Guesses: 3753
Total Time: 1.22616 seconds
Average Guess # until solve : 3.75300
Solve Percentage : 98.6%
---------------------------------
```

### Exported Data

The script exports the following data to the `output/test.csv` file:

- Game Number
- Number of Guesses Made
- Puzzle Solved (True/False)
- Time Taken to Solve (in seconds)
- Solution Word
- First Guess Result

## Finding The Best Starting Word `compare.py`

This part of the project focuses on simulating Wordle games and comparing different starting words' performance.
The compare.py script allows you to test various starting words and evaluates their effectiveness in solving Wordle puzzles efficiently.

### Usage

Prepare a list of starting words: Create a text file (startwords.txt) containing a list of words you want to test as initial guesses.

Run the script: Execute the script with the prepared list of starting words. For each word in the list, the script simulates a specified number of Wordle games (e.g., 100) with that word as the initial guess.

Results and Comparison: The script collects data on the average number of guesses required to solve the puzzle and the solve percentage for each starting word.
This data will be saved to `output/starting_words.csv` for processing.

### Example Output

```
Testing word: hello
Avg Guesses per game: 3.12
Solve Percentage : 95.00%
Simulation Time: 1.234 seconds
--------------------------------------------------
Testing word: puzzle
Avg Guesses per game: 3.40
Solve Percentage : 97.50%
Simulation Time: 1.345 seconds
--------------------------------------------------
Testing word: slate
Avg Guesses per game: 3.13
Solve Percentage : 98.20%
Simulation Time: 1.045 seconds
--------------------------------------------------
...
Avg Attempts for starting word:
hello: 3.12
puzzle: 3.40
slate
...

Data list saved to starting_words_data.csv
```

## Wordle Data Analysis and Visualization `graph.py`

This part of the project focuses on analyzing and visualizing Wordle game data. The graph.py script reads game data from a CSV file,
performs various analysis and visualizations.

- #### Solve Percentage Pie Chart
  <img width=500 src="./imgs/piechartsolvestatus.png">
- #### Number of Guesses Bar Plot
  <img width=500 src="./imgs/barplotnumguesses.png">
- #### Number of Guesses Histogram
  <img width=500 src="./imgs/histogramnumguesses.png">
- #### Number of Guesses Box Plot
  <img width=500 src="./imgs/boxplotnumguesses.png">
- #### Number of Guesses Error Bars
  <img width=500 src="./imgs/errorbars.png">
- #### Number of Guesses Violin Plot
  <img width=500 src="./imgs/violinplot.png">
- #### Time Per Game Scatter Plot
  <img width=500 src="./imgs/scatterplottimepergame.png">
- #### Time vs The Number of Guesses Scatter Plot
  <img width=500 src="./imgs/scatterplottimvsnumguesses.png">
- #### Letter Frequency in Solution Words Bar Plot
  <img width=500 src="./imgs/barplotletterfreq.png">
- #### Top 50 First Result Distribution Bar plot
  <img width=500 src="./imgs/barchartfirstresult.png">
- #### First Result Categories Pie Chart
  <img width=500 src="./imgs/piechartfirstresult.png">
- #### Starting Result -> Number of Guesses Heatmap
  <img width=500 src="./imgs/heatmapstartingresult.png">
- #### Number of 'w's in starting Result vs Number of Guesses Scatter Plot
  <img width=500 src="./imgs/scatterplotfirstresultvsnumguesses.png">
- #### Top 10 Most Frequent Words Bar Chart
  <img width=500 src="./imgs/wordfreqbarchart.png">
- #### Word Cloud of Solution Word Frequency
  <img width=500 src="./imgs/wordcloudsolutionwords.png">
- #### Solution word to Average Guesses Bar Chart
  <img width=500 src="./imgs/barplotstartingwordsvsavgguess.png">

## Installation

#### 1. Download repository

      git clone https://github.com/josephjquinn/word-wise.git

#### 2. Install required packages

     pip install -r requirements.txt

#### 3. Run program

      python {script_name}.py
