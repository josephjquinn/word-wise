import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import numpy as np
import seaborn as sns
import pandas as pd
from helper import read_data


# Function to create a line plot representing time taken per game
def create_time_line_plot(header, data):
    time_taken_index = header.index('Time Taken (seconds)')
    game_numbers = range(1, len(data) + 1)
    time_per_game = [float(row[time_taken_index]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(game_numbers, time_per_game, marker='o', linestyle='-')
    plt.xlabel('Game Number')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Time per Game')
    plt.grid(True)
    plt.show()


# Function to create a box plot representing time per game by solved status
def create_time_box_plot(header, data):
    time_taken_index = header.index('Time Taken (seconds)')
    puzzle_solved_index = header.index('Puzzle Solved')

    solved_times = [float(row[time_taken_index]) for row in data if row[puzzle_solved_index] == 'True']
    unsolved_times = [float(row[time_taken_index]) for row in data if row[puzzle_solved_index] == 'False']

    plt.figure(figsize=(10, 6))
    plt.boxplot([solved_times, unsolved_times], labels=['Solved', 'Unsolved'])
    plt.xlabel('Solved Status')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Box Plot of Time per Game by Solved Status')
    plt.grid(True)
    plt.show()


# Function to create a scatter plot for time vs. number of guesses
def create_scatter_plot(header, data):
    num_guesses_index = header.index('Number of Guesses')
    time_taken_index = header.index('Time Taken (seconds)')

    num_guesses = [int(row[num_guesses_index]) for row in data]
    time_taken = [float(row[time_taken_index]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.scatter(num_guesses, time_taken, alpha=0.5)
    plt.xlabel('Number of Guesses')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Scatter Plot of Time vs. Number of Guesses')
    plt.grid(True)
    plt.show()


# Function to create a histogram representing number of guesses per game and to show the bell curve
def create_histogram(header, data, bin_width=1):
    num_guesses_index = header.index('Number of Guesses')
    num_guesses = [int(row[num_guesses_index]) for row in data]

    # Create two lists for the data: "Solved" and "Unsolved"
    solved_guesses = [guess for guess in num_guesses if guess < 7]
    unsolved_guesses = [7] * num_guesses.count(7)  # Assuming 7 represents unsolved games

    # Calculate the range of values for the x-axis (including 7)
    x_values = list(range(min(num_guesses), max(num_guesses) + bin_width, bin_width))

    plt.figure(figsize=(10, 6))
    # Plot the histogram for solved and unsolved guesses
    plt.hist([solved_guesses, unsolved_guesses], bins=x_values, alpha=0.75, edgecolor='black', label=['Solved', 'Unsolved'])

    # Create a normal distribution (bell curve) for all guesses
    mu = np.mean(num_guesses)
    sigma = np.std(num_guesses)
    curve_x = np.linspace(min(num_guesses), max(num_guesses), 100)
    curve_y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(curve_x - mu)**2 / (2 * sigma**2))

    # Plot the bell curve
    plt.plot(curve_x, curve_y * len(num_guesses) * bin_width, color='red', linestyle='dashed', linewidth=2, label='Bell Curve')

    plt.xlabel('Number of Guesses')
    plt.ylabel('Frequency')
    plt.title('Histogram of Number of Guesses with Bell Curve')
    plt.legend()
    plt.grid(True)
    plt.show()


# Function to create a bar chart representing number of guesses per game
def create_bar_graph_with_unsolved_section(header, data, bin_width=1):
    num_guesses_index = header.index('Number of Guesses')
    num_guesses = [int(row[num_guesses_index]) for row in data]

    # Create two lists for the data: "Solved" and "Unsolved"
    solved_guesses = [guess for guess in num_guesses if guess != 7]
    unsolved_guesses = [7] * num_guesses.count(7)  # Assuming 7 represents unsolved games

    # Calculate the range of values for the x-axis (excluding 7)
    x_values = list(range(min(solved_guesses), max(solved_guesses) + bin_width, bin_width))

    # Calculate the frequencies for each bin
    bin_frequencies = []
    for x in x_values:
        bin_frequencies.append(solved_guesses.count(x))

    # Add a separate "Unsolved" column if 7 is present in the data
    if 7 in num_guesses:
        x_values.append(max(solved_guesses) + bin_width)  # Position "Unsolved" to the right of the last bar
        bin_frequencies.append(unsolved_guesses.count(7))

    # Convert x-values to strings for "Unsolved"
    x_labels = [str(label) if label != max(solved_guesses) + bin_width else 'Unsolved' for label in x_values]

    plt.figure(figsize=(10, 6))
    plt.bar(x_values, bin_frequencies, width=bin_width, alpha=0.75, edgecolor='black')

    plt.xlabel('Number of Guesses')
    plt.ylabel('Frequency')
    plt.title('Number of Guesses Frequency')
    plt.grid(True)

    # Set custom x-axis labels
    plt.xticks(x_values, x_labels)

    plt.show()


# function to calculate solution word frequency
def calculate_word_frequencies(data, solution_word_column_index):
    solution_words = [row[solution_word_column_index] for row in data]
    word_frequency = Counter(solution_words)
    return word_frequency


# Function to create a bar chart for solution word frequency
def create_word_frequency_bar_chart(word_frequency, top_n=10):
    # Get the top N most frequent words and their frequencies
    top_words = [word for word, frequency in word_frequency.most_common(top_n)]
    top_frequencies = [frequency for word, frequency in word_frequency.most_common(top_n)]

    plt.figure(figsize=(12, 6))
    plt.barh(top_words, top_frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Invert y-axis to display most frequent words at the top
    plt.show()


# Function to create a word cloud for solution word frequency
def create_word_cloud(word_frequency):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequency)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Solution Word Frequency')
    plt.show()


# Function to create pie chart representing solve percentage
def generate_pie_chart(header, data):
    puzzle_solved_index = header.index('Puzzle Solved')

    solved_count = sum(1 for row in data if row[puzzle_solved_index] == 'True')
    unsolved_count = sum(1 for row in data if row[puzzle_solved_index] == 'False')

    # Data for the pie chart
    labels = ['Solved', 'Unsolved']
    sizes = [solved_count, unsolved_count]
    colors = ['green', 'red']
    explode = (0.1, 0)  # Explode the first slice (Solved)

    # Create the pie chart
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Puzzle Solved Status')

    # Show the pie chart
    plt.show()


# Function to create a box plot representing number of guesses per game
def create_box_plot(header, data):
    num_guesses_column = header.index('Number of Guesses')
    num_guesses_data = [int(row[num_guesses_column]) for row in data]

    plt.figure(figsize=(8, 6))
    plt.boxplot(num_guesses_data, vert=False)
    plt.xlabel('Number of Guesses')
    plt.title('Box Plot of Number of Guesses')
    plt.grid(True)
    plt.show()


# Function to create scatter plot representing time taken per number of guesses
def create_scatter_plot(header, data):
    time_taken_column = header.index('Time Taken (seconds)')
    num_guesses_column = header.index('Number of Guesses')

    time_taken_data = [float(row[time_taken_column]) for row in data]
    num_guesses_data = [int(row[num_guesses_column]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.scatter(time_taken_data, num_guesses_data, alpha=0.5)
    plt.xlabel('Time Taken (seconds)')
    plt.ylabel('Number of Guesses')
    plt.title('Scatter Plot of Time vs. Number of Guesses')
    plt.grid(True)
    plt.show()


# Function to create error bar graph of number of guesses data column
def create_error_bar_plot(header, data):
    num_guesses_column = header.index('Number of Guesses')

    num_guesses_data = [int(row[num_guesses_column]) for row in data]

    # Calculate means and standard errors (you can adjust the error calculation as needed)
    means = num_guesses_data
    std_errors = np.random.uniform(1, 2, len(means))  # Replace with your error calculation

    x = np.arange(len(means))
    width = 0.35  # Width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, means, width, yerr=std_errors, align='center', alpha=0.75, edgecolor='black', capsize=5)
    ax.set_xlabel('Game #')
    ax.set_ylabel('Number of Guesses')
    ax.set_title('Error Bar Plot of Number of Guesses (Without Confidence Intervals)')
    ax.set_xticks(x)
    ax.grid(True)

    plt.show()


# Function to create a violin plot representing number of guesses
def create_violin_plot(header, data):
    num_guesses_column = header.index('Number of Guesses')

    num_guesses_data = [int(row[num_guesses_column]) for row in data]

    plt.figure(figsize=(10, 6))
    sns.violinplot(data=num_guesses_data, orient='v', inner='box')
    plt.xlabel('Games')
    plt.ylabel('Number of Guesses')
    plt.title('Violin Plot of Guess Distributions')
    plt.grid(True)
    plt.show()


# Function to create bar chart representing solution word frequency
def create_solution_word_letter_frequency_bar_chart(header, data):
    solution_words_column = header.index('Solution Word')

    solution_words = [row[solution_words_column] for row in data]

    # Calculate the frequency of each letter in the solution words
    letter_frequency_data = Counter(''.join(solution_words).lower())

    # Extract letters and frequencies
    letters = list(letter_frequency_data.keys())
    frequencies = list(letter_frequency_data.values())

    # Create the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(letters, frequencies)
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.title('Letter Frequency in Solution Words')
    plt.grid(axis='y')
    plt.xticks(rotation=90)
    plt.show()


# Function to create pie chart representing first result string frequency
def create_pie_chart(header, data, top_n=20):
    first_result_category_column = header.index('First Result')

    # Count the occurrences of each category
    category_counts = {}
    for row in data:
        category = row[first_result_category_column]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    # Sort categories by count in descending order
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    # Prepare data for the pie chart
    categories = [category[0] for category in sorted_categories[:top_n]]
    counts = [category[1] for category in sorted_categories[:top_n]]

    # Group remaining categories into an "Others" category
    if len(sorted_categories) > top_n:
        categories.append('Others')
        counts.append(sum(category[1] for category in sorted_categories[top_n:]))

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Pie Chart of First Result Categories')
    plt.show()


# Function to create bar chart showing the first result frequency
def create_bar_chart_of_first_results(header, data, top_n=50):
    first_result_column = header.index('First Result')

    # Count the occurrences of each first result
    first_result_counts = {}
    for row in data:
        first_result = row[first_result_column]
        if first_result in first_result_counts:
            first_result_counts[first_result] += 1
        else:
            first_result_counts[first_result] = 1

    # Sort first results by count in descending order
    sorted_results = sorted(first_result_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Prepare data for the bar chart
    first_results = [result[0] for result in sorted_results]
    counts = [result[1] for result in sorted_results]

    # Create the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(first_results, counts, alpha=0.75, edgecolor='black')
    plt.xlabel('First Result')
    plt.ylabel('Frequency')
    plt.title(f'Bar Chart of Top {top_n} First Result Distribution')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()


# Function to create heatmap showing the relationship between starting result and number of guesses
def create_heatmap_for_starting_results_vs_guesses(header, data, top_n=20):
    starting_result_column = header.index('First Result')
    guesses_column = header.index('Number of Guesses')

    # Create a list of starting results
    starting_results = [row[starting_result_column] for row in data]

    # Calculate the frequency of each starting result
    starting_result_counts = Counter(starting_results)

    # Get the top N most common starting results
    top_starting_results = starting_result_counts.most_common(top_n)

    # Extract unique guesses from the data
    unique_guesses = sorted(set(row[guesses_column] for row in data))

    # Create a matrix to store the frequency of combinations
    frequency_matrix = np.zeros((len(top_starting_results), len(unique_guesses)))

    for i, (starting_result, _) in enumerate(top_starting_results):
        for j, guesses in enumerate(unique_guesses):
            # Count the occurrences of the combination
            count = sum(1 for row in data if row[starting_result_column] == starting_result and row[guesses_column] == guesses)
            frequency_matrix[i][j] = count

    # Create the heatmap
    plt.figure(figsize=(12, 8))
    plt.imshow(frequency_matrix, cmap='viridis', aspect='auto', origin='upper')
    plt.colorbar(label='Frequency')
    plt.xlabel('Number of Guesses')
    plt.ylabel('Starting Results')
    plt.title('Starting Results vs. Number of Guesses')
    plt.xticks(np.arange(len(unique_guesses)), unique_guesses, rotation=90)
    plt.yticks(np.arange(len(top_starting_results)), [item[0] for item in top_starting_results])
    plt.show()


# Function to create scatter plot showing the relationship between first result and number of guesses
def create_scatter_plot_for_w_vs_guesses(header, data):
    starting_result_column = header.index('First Result')
    guesses_column = header.index('Number of Guesses')

    # Extract 'w' counts from starting results and number of guesses
    w_counts = []
    num_guesses = []

    for row in data:
        starting_result = row[starting_result_column]
        guesses = row[guesses_column]

        w_count = starting_result.count('w')  # Count 'w's in the starting result
        w_counts.append(w_count)
        num_guesses.append(guesses)

    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(w_counts, num_guesses, alpha=0.5)

    plt.xlabel('Number of "w"s in Starting Result')
    plt.ylabel('Number of Guesses')
    plt.title('Scatter Plot of "w"s in Starting Result vs. Number of Guesses')
    plt.grid(True)
    plt.show()


# Function to create bar chart representing the relationship between start word and avg number of guesses
def plot_bar_chart_from_csv(csv_file):
    df = pd.read_csv(csv_file, header=None, delimiter=',')

    # Extract the starting words and average guesses columns from the DataFrame
    starting_words = df.iloc[:, 0]
    avg_guesses_list = df.iloc[:, 1]

    # Sort the data by average guesses in ascending order
    sorted_indices = avg_guesses_list.argsort()
    starting_words = starting_words.iloc[sorted_indices]
    avg_guesses_list = avg_guesses_list.iloc[sorted_indices]

    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

    # Bar chart with green bars
    plt.bar(starting_words, avg_guesses_list, alpha=0.7, color='green')

    plt.xlabel('Starting Words')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.ylabel('Average Guesses per Game')
    plt.title('Relationship between Starting Words and Average Guesses')
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()  # Ensure labels and ticks fit nicely
    plt.show()


if __name__ == "__main__":

# Reading Data
    file_path = "../data/test_data.csv"
    header, data = read_data(file_path)


# Creating Graphs
    create_box_plot(header, data)
    create_scatter_plot(header, data)
    create_error_bar_plot(header, data)
    create_violin_plot(header, data)
    create_solution_word_letter_frequency_bar_chart(header, data)
    create_pie_chart(header, data)
    create_bar_chart_of_first_results(header, data)
    create_heatmap_for_starting_results_vs_guesses(header, data)
    create_scatter_plot_for_w_vs_guesses(header, data)
    generate_pie_chart(header, data)
    create_time_line_plot(header, data)
    create_time_box_plot(header, data)
    create_scatter_plot(header, data)
    create_bar_graph_with_unsolved_section(header, data, bin_width=1)
    solution_word_column_index = header.index('Solution Word')
    word_frequency = calculate_word_frequencies(data, solution_word_column_index)
    create_word_frequency_bar_chart(word_frequency)
    create_word_cloud(word_frequency)
    create_histogram(header, data)
    plot_bar_chart_from_csv('../data/starting_words_data.csv')
