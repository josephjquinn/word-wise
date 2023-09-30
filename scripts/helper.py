from bs4 import BeautifulSoup
import csv


def get_wordle_guesses():
    words = []
    with open("../data/wordlist.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words


def read_data(file_path):
    data = []  # Initialize an empty list to store data

    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # Read the header row

        # Iterate through each row and append to the data list
        for row in csv_reader:
            data.append(row)

    return header, data


def parseHTML(html_content, row_number):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the row-0 div
    row_id = f'row-{row_number}'
    row = soup.find('row', {'id': row_id})

    code = []
    count = 0
    print(row)
    for box in row.find_all('box'):
        box_class = box.get('class')[0]  # Get the first class of the 'box' element
        if box_class == "wrongLetter":
            code.append('w')
        elif box_class == "rightSpot":
            code.append('g')
        elif box_class == "wrongSpot":
            code.append('y')
        count += 1
    return code

# Function to export data to csv format
def export_to_csv(num_guesses, puzzle_solved, game_times, solution_words, first_results):
    file_path = "../data/test_data.csv"
    game_numbers = list(range(1, len(num_guesses) + 1))

    # Combine game data including the first result string
    game_data = list(zip(game_numbers, num_guesses, puzzle_solved, game_times, solution_words, first_results))

    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Game #', 'Number of Guesses', 'Puzzle Solved', 'Time Taken (seconds)', 'Solution Word',
                             'First Result'])  # Include the new column
        csv_writer.writerows(game_data)

    print(f'Data has been exported to {file_path}')