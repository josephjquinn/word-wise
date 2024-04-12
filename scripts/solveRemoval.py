import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from helper import get_wordle_guesses


class WordleTests:
    word_list = []

    # You can change this to your preferred WebDriver
    def __init__(self, show_browser=True):
        chrome_options = Options()
        if not show_browser:
            chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        self.show_browser = show_browser

    # version 1 of my algorithm, removes words with impossible probabilities, no wordscore implemented
    def modify_word_list(self, word, letter_status):
        new_word_list = []
        correct_letters = []
        present_letters = []
        for i in range(len(word)):
            if letter_status[i] == "correct":
                correct_letters.append(word[i])
                for w in self.word_list:
                    if w[i] == word[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []
        for i in range(len(word)):
            if letter_status[i] == "present":
                present_letters.append(word[i])
                for w in self.word_list:
                    if word[i] in w and word[i] != w[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []
        for i in range(len(word)):
            if letter_status[i] == "absent":
                if word[i] not in correct_letters and word[i] not in present_letters:
                    for w in self.word_list:
                        if word[i] not in w:
                            new_word_list.append(w)
                else:
                    for w in self.word_list:
                        if word[i] != w[i]:
                            new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []

    # launches NYT wordle and runs algorithm
    def solve_wordle(self):
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

        self.word_list = get_wordle_guesses()
        random.seed()
        word = random.choice(self.word_list)
        num_attempts = 0
        found_word = False
        for attempt in range(6):
            num_attempts += 1
            if len(self.word_list) == 0:
                print("Today's word was not found in my dictionary!")
                break
            word = random.choice(self.word_list)
            letters = []
            for letter in word:
                letters.append(letter)
                button = f'button[data-key="{letter}"]'
                self.driver.find_element(By.CSS_SELECTOR, button).click()
            button = 'button[class*="oneAndAHalf"]'
            self.driver.find_element(By.CSS_SELECTOR, button).click()
            row = f'div[class*="Board"] div[class*="Row-module"]:nth-of-type({num_attempts})'
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
                break
            self.word_list.remove(word)
            self.modify_word_list(word, letter_status)

        print("---------------------------")
        if found_word:
            print('Word: "%s"\nAttempts: %s' % (word.upper(), num_attempts))
        else:
            print('Final guess: "%s" (Not the correct word!)' % word.upper())
            print("Unable to solve for the correct word in 6 attempts!")
        print("---------------------------")

    # Closes website
    def close_browser(self):
        self.driver.quit()


# Runs program
if __name__ == "__main__":
    show_browser = input("Show browser window? (y/n): ").lower() == "y"
    wordle_test = WordleTests(show_browser)
    wordle_test.solve_wordle()
    wordle_test.close_browser()
