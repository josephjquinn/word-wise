import random
import time
from algorithm import word_remover, bestWord, letterFreq
from helper import get_wordle_guesses, export_to_csv


# Generate a random 5-letter word as the solution
def generate_solution_word():
    word_list = get_wordle_guesses()
    return random.choice(word_list)


# wordle game logic
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
            ans[i] = "#"

    # Sets each position in yellow list to '1' if the letter is in the correct position in the key but not in the correct position.
    # Then removes the letter from the key list by replacing it with '#'.
    for i in range(5):
        for j in range(5):
            if guess[i] == ans[j] and green[i] != 1:
                yellow[i] = 1
                ans[j] = "#"

    # Sets each position in white list to '1' if the letter is not in the key at all.
    # It does this by a series of eliminations with the yellow and green lists.
    for i in range(5):
        if yellow[i] == green[i]:
            white[i] = 1

    # Convert green, yellow, and white lists into a single string
    result_string = "".join(
        ["g" if g == 1 else "y" if y == 1 else "w" for g, y in zip(green, yellow)]
    )

    return result_string


# Simulation loop
def run_game(games):
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
        guess = "slate"
        first_word_result = evaluate_guess(guess, solution_word)
        possible_words = get_wordle_guesses()  # Replace with your word list generator
        counter = 1
        while counter < 7:
            result = evaluate_guess(guess, solution_word)

            if result == "ggggg":
                print(solution_word)
                solved = True
                solve_count += 1
                break  # The game is won

            possible_words = word_remover(
                result, guess, possible_words
            )  # Replace with your algorithm

            suggestion = bestWord(
                possible_words, letterFreq(possible_words)
            )  # Replace with your algorithm
            guess = suggestion
            counter += 1
        if solved == False:
            print("unsolved")

        # Data Tracking
        num_guesses.append(counter)
        end_time = time.time()
        elapsed_time = end_time - start_time
        game_times.append(elapsed_time)
        first_results.append(first_word_result)

        puzzle_solved.append(solved)
        solution_words.append(solution_word)
        total_guesses = total_guesses + counter

    # Print the number of guesses made for each game
    end_simulation_time = time.time()
    total_simulation_time = end_simulation_time - start_simulation_time
    print("Game Results:")
    for i, (guesses, time_taken) in enumerate(zip(num_guesses, game_times), start=1):
        print(
            f"Game {i}: {guesses} guesses, Time Taken: {time_taken:.5f} seconds, Solved: {puzzle_solved[i - 1]}"
        )
    print("\n---------------------------------")
    print(f"Total Guesses: {total_guesses}")
    print(f"Total Time: {total_simulation_time:.5f} seconds")
    print(f"Average Guess # until solve : {total_guesses / games:.5f}")
    print(f"Solve Percentage : {(solve_count / games) * 100:.1f}%")
    print("---------------------------------")
    export_to_csv(num_guesses, puzzle_solved, game_times, solution_words, first_results)


if __name__ == "__main__":
    run_game(
        1000
    )  # <- change this value to determine how many game you want to run per word
