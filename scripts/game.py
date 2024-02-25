import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from helper import parseHTML, get_wordle_guesses
from algorithm import word_remover, bestWord, letterFreq


class WordleTests:

    # initializer
    def __init__(self):
        self.driver = webdriver.Chrome()

    # function to click on an on-screen element
    def click(self, element):
        element.click()

    # extracts page html
    def get_page_source(self):
        return self.driver.page_source

    # game loop
    def run_game(self, games):
        for i in range(games):
            self.possible_words = get_wordle_guesses()

            self.driver.get("https://wordle-vanilla.vercel.app/index.html")

            guess = "slate"
            letters = []

            for letter in guess:
                letters.append(letter)
                element = self.driver.find_element(
                    By.CSS_SELECTOR, f'button[id="{letter}"]'
                )
                self.click(element)

            element = self.driver.find_element(By.CSS_SELECTOR, 'button[id*="enter"]')
            self.click(element)
            time.sleep(2)

            html_content = self.get_page_source()
            letter_status = parseHTML(html_content, 0)
            result = "".join(letter_status)

            counter = 0
            while result != "ggggg" and counter < 5:
                self.possible_words = word_remover(result, guess, self.possible_words)
                suggestion = bestWord(
                    self.possible_words, letterFreq(self.possible_words)
                )
                letters = []
                guess = suggestion

                for letter in guess:
                    letters.append(letter)
                    element = self.driver.find_element(
                        By.CSS_SELECTOR, f'button[id="{letter}"]'
                    )
                    self.click(element)

                element = self.driver.find_element(
                    By.CSS_SELECTOR, 'button[id*="enter"]'
                )
                self.click(element)
                time.sleep(2)

                html_content = self.get_page_source()
                letter_status = parseHTML(html_content, counter + 1)
                result = "".join(letter_status)
                counter += 1

            time.sleep(4)

            print(f"Game {i+1}: Word: {guess}, Attempts: {counter+1}")

            element = self.driver.find_element(By.CSS_SELECTOR, 'button[id="newGame"]')
            self.click(element)


if __name__ == "__main__":
    wordle_test = WordleTests()
    wordle_test.run_game(
        10
    )  # <- change this value to determine how many game you want to run
