import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # get result

    def get_result(self, attempt):
        row = f'div[class*="Board"] div[class*="Row-module"]:nth-of-type({attempt})'
        tile = row + ' div:nth-child(%s) div[class*="module_tile__"]'
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, tile % "5" + '[data-state$="t"]')
            )
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, tile % "5" + '[data-animation="idle"]')
            )
        )
        letter_status = []
        for i in range(1, 6):
            letter_eval = self.driver.find_element(
                By.CSS_SELECTOR, tile % str(i)
            ).get_attribute("data-state")
            letter_status.append(letter_eval)
        if letter_status.count("correct") == 5:
            found_word = True

        resultData = ""
        for res in letter_status:
            if res == "correct":
                resultData += "g"
            elif res == "absent":
                resultData += "w"
            elif res == "present":
                resultData += "y"

        return resultData

    def userInput(self):
        intput = "enter word"
        return input

    # game loop
    def solve(self, input):
        self.possible_words = get_wordle_guesses()

        self.driver.get("https://www.nytimes.com/games/wordle/index.html")

        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.purr-blocker-card__button")
                )
            )
            element.click()
        except:
            pass

        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "Welcome-module_button__ZG0Zh")
                )
            )
            element.click()
        except:
            pass

        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'svg[data-testid="icon-close"]')
                )
            )
            element.click()
        except:
            pass

        self.driver.execute_script(
            "document.querySelectorAll('div.place-ad').forEach(function(el) { el.remove(); });"
        )

        guess = input
        letters = []

        for letter in guess:
            letters.append(letter)
            button = f'button[data-key="{letter}"]'
            self.driver.find_element(By.CSS_SELECTOR, button).click()

        button = 'button[class*="oneAndAHalf"]'
        self.driver.find_element(By.CSS_SELECTOR, button).click()
        counter = 1
        result = self.get_result(1)

        counter = 2
        while result != "ggggg" and counter < 7:
            self.possible_words = word_remover(result, guess, self.possible_words)
            suggestion = bestWord(self.possible_words, letterFreq(self.possible_words))
            letters = []
            guess = suggestion

            for letter in guess:
                letters.append(letter)
                button = f'button[data-key="{letter}"]'
                self.driver.find_element(By.CSS_SELECTOR, button).click()

            button = 'button[class*="oneAndAHalf"]'
            self.driver.find_element(By.CSS_SELECTOR, button).click()

            result = self.get_result(counter)
            counter += 1

        print("---------------------------")
        if result == "ggggg":
            print('Word: "%s"\nAttempts: %s' % (guess.upper(), counter - 1))
        else:
            print('Final guess: "%s" (Not the correct word!)' % guess.upper())
            print("Unable to solve for the correct word in 6 attempts!")
        print("---------------------------")


if __name__ == "__main__":
    user_input = ""
    while len(user_input) != 5:
        user_input = input("Enter a 5-letter word: ")
        if len(user_input) != 5:
            print("Please enter exactly 5 letters.")
    wordle_test = WordleTests()
    wordle_test.solve(user_input.lower())
