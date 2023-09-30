import random
import time
import csv

from algorithm import get_wordle_guesses, word_remover, bestWord, letterFreq
from helper import get_wordle_guesses

# Functions for simulating Wordle game logic
def generate_solution_word():
    # Generate a random 5-letter word as the solution
    word_list = get_wordle_guesses()
    return random.choice(word_list)


def evaluate_guess(word, key):
    # Setting up method variables and lists
    guess = list(word)
    ans = list(key)
    green = [0] * 5
    yellow = [0] * 5
    white = [0] * 5

    # Sets each position in green list to '1' if the letter is in the key and in the correct position in the key.
    # Then removes the letter from the key list by replacing it with '#'.
    for i in range(5):
        if guess[i] == ans[i]:
            green[i] = 1
            ans[i] = '#'

    # Sets each position in yellow list to '1' if the letter is in the correct position in the key but not in the correct position.
    # Then removes the letter from the key list by replacing it with '#'.
    for i in range(5):
        for j in range(5):
            if guess[i] == ans[j] and green[i] != 1:
                yellow[i] = 1
                ans[j] = '#'

    # Sets each position in white list to '1' if the letter is not in the key at all.
    # It does this by a series of eliminations with the yellow and green lists.
    for i in range(5):
        if yellow[i] == green[i]:
            white[i] = 1

    # Convert green, yellow, and white lists into a single string
    result_string = ''.join(['g' if g == 1 else 'y' if y == 1 else 'w' for g, y in zip(green, yellow)])

    return result_string


def run_game(games, start_word):
    start_simulation_time = time.time()
    game_times = []
    num_guesses = []
    solution_words = []
    puzzle_solved = []
    first_results = []
    total_guesses = 0
    solve_count = 0

    for _ in range(games):
        start_time = time.time()

        solved = False
        solution_word = generate_solution_word()
        first_word = start_word
        guess = first_word
        first_word_result = evaluate_guess(first_word, solution_word)
        possible_words = get_wordle_guesses()  # Replace with your word list generator
        counter = 1

        while counter < 7:
            result = evaluate_guess(guess, solution_word)

            if result == "ggggg":
                solved = True
                solve_count += 1
                break  # The game is won

            possible_words = word_remover(result, guess, possible_words)  # Replace with your algorithm

            suggestion = bestWord(possible_words, letterFreq(possible_words))  # Replace with your algorithm
            guess = suggestion
            counter += 1

        total_guesses = total_guesses + counter

    # Print the number of guesses made for each game
    end_simulation_time = time.time()
    total_simulation_time = end_simulation_time - start_simulation_time
    starting_word_avg_guesses = total_guesses / games
    print("Avg Guesses per game: ", starting_word_avg_guesses)
    starting_word_solve_percentage = (solve_count/games) * 100
    print(f"Solve Percentage : {starting_word_solve_percentage}%")
    print(f"Simulation Time: {total_simulation_time:.3f} seconds")

    return starting_word_avg_guesses


def write_guess_list_to_csv(guess_list, output_file):
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for word, avg_score in guess_list:
            writer.writerow([word, avg_score])

def read_start_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

if __name__ == "__main__":
    guess_list = []
    start_words = read_start_words("../data/startwords.txt")
    for word in start_words:
        print(f"Testing word: {word}")
        score = run_game(100, word)  # Run 10 games for each word with the word as the initial guess
        guess_list.append((word, score))
        print("-" * 50)

    # Print the average guesses per game for each word
    print("Avg Attempts for starting word: ")
    for word, avg_score in guess_list:
        print(f"{word}: {avg_score:.2f}")
    output_file = "../data/starting_words_data.csv"
    write_guess_list_to_csv(guess_list, output_file)
    print(f"Data list saved to {output_file}")