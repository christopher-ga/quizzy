import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument("--window-size=300,900")
    return webdriver.Chrome(options=chrome_options)


def setup_firefox():
    driver = webdriver.Firefox()
    driver.set_window_position(800, 0)
    driver.set_window_size(1024, 768)
    return driver


def wait_and_click(driver, by, value):
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((by, value))).click()
    except TimeoutException:
        logger.error(f"Timeout waiting for element to be clickable: {by}, {value}")
    except NoSuchElementException:
        logger.error(f"Element not found: {by}, {value}")


def create_quiz(driver, name, category_value):
    try:
        # open the create quiz window
        create_btn = driver.find_element(By.CSS_SELECTOR, value='.create-option')
        create_btn.click()

        # input the name
        name_input = driver.find_element(By.NAME, value='create_name')
        name_input.send_keys(name)

        # select quiz category
        select = Select(driver.find_element(By.CSS_SELECTOR, value='select.form-control.dropdown'))
        select.select_by_value(category_value)

        # start quiz
        join_quiz_btn = driver_chrome.find_element(By.NAME, value='create')
        join_quiz_btn.click()

        # check game pin
        game_pin_element = driver_chrome.find_element(By.CSS_SELECTOR, value='.pin h1')
        return game_pin_element.text

    except Exception as e:
        logger.error(f"An error occurred during quiz creation: {e}")


def join_quiz(driver, name, game_pin):
    try:
        # open the join quiz window
        join_btn = driver.find_element(By.CSS_SELECTOR, value='.join-option')
        join_btn.click()

        # input the name
        join_name_input = driver.find_element(By.NAME, value='join_name')
        join_name_input.send_keys(name)
        #
        # input the game pin
        join_name_input = driver.find_element(By.NAME, value='code')
        join_name_input.send_keys(game_pin)
        #
        # join quiz
        join_quiz_btn = driver.find_element(By.NAME, value='join')
        join_quiz_btn.click()

    except Exception as e:
        logger.error(f"An error occurred during quiz joining: {e}")


def force_start(driver):
    start_button = driver.find_element(By.CSS_SELECTOR, value='button')
    start_button.click()


def answer_quiz_questions(driver_1, driver_2):
    option_ids = ["a", "b", "c", "d"]
    for i in range(10):
        # driver 1
        random_btn_id = random.choice(option_ids)
        wait_and_click(driver_1, By.CSS_SELECTOR, f"[value='{random_btn_id}']")

        # driver 2
        random_btn_id = random.choice(option_ids)
        wait_and_click(driver_2, By.CSS_SELECTOR, f"[value='{random_btn_id}']")
        time.sleep(8)


if __name__ == "__main__":
    link = 'http://localhost:6002/'

    driver_chrome = setup_chrome()
    driver_firefox = setup_firefox()
    driver_chrome.get(link)
    driver_firefox.get(link)

    try:
        game_pin = create_quiz(driver_chrome, 'Celina', '9')
        join_quiz(driver_firefox, 'Balbina', game_pin)
        force_start(driver_firefox)
        answer_quiz_questions(driver_chrome, driver_firefox)

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    finally:
        time.sleep(30)
        driver_chrome.quit()
        driver_firefox.quit()
