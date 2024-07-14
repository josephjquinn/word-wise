from bs4 import BeautifulSoup
import csv
import os


def get_wordle_guesses():
    words = []
    with open("./data/wordlist.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words


def read_data(file_path):
    data = []

    with open(file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)

        for row in csv_reader:
            data.append(row)

    return header, data


def parseHTML(html_content, row_number):
    soup = BeautifulSoup(html_content, "html.parser")

    row_id = f"row-{row_number}"
    row = soup.find("row", {"id": row_id})

    code = []
    count = 0
    for box in row.find_all("box"):
        box_class = box.get("class")[0]
        if box_class == "wrongLetter":
            code.append("w")
        elif box_class == "rightSpot":
            code.append("g")
        elif box_class == "wrongSpot":
            code.append("y")
        count += 1
    return code


def export_to_csv(
    num_guesses, puzzle_solved, game_times, solution_words, first_results
):
    file_path = "./output/test.csv"
    os.makedirs("./output", exist_ok=True)
    game_numbers = list(range(1, len(num_guesses) + 1))

    game_data = list(
        zip(
            game_numbers,
            num_guesses,
            puzzle_solved,
            game_times,
            solution_words,
            first_results,
        )
    )

    with open(file_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            [
                "Game #",
                "Number of Guesses",
                "Puzzle Solved",
                "Time Taken (seconds)",
                "Solution Word",
                "First Result",
            ]
        )
        csv_writer.writerows(game_data)

    print(f"Data has been exported to {file_path}")
