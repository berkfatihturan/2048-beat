import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException

import numpy as np

chrome_driver_path = "D:\BFT\Project\Python\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

MOVE = [Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT]
WAIT_TIME = 0


def deneme(arr) -> list:  # too slow

    for i, chosen in enumerate(arr):
        for t, compare in enumerate(arr[i + 1:]):
            if compare[0] > chosen[0]:
                arr[i] = compare
                arr[i + 1 + t] = chosen
                chosen = compare

    return arr


def get_cells() -> list:
    item_list = []

    try:
        item_container = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[3]")
        for a in item_container.find_elements(By.CSS_SELECTOR, "div .tile"):
            power = int(a.get_attribute("class").split()[1].split("-")[1])  # get number
            position = a.get_attribute("class").split()[2].split("-")[2:]  # get position
            item_list.append([power, int(position[0]), int(position[1])])  # add to list
    except StaleElementReferenceException:  # if page not reload
        print("Oops!")
        return get_cells()

    # sort to highest to lowest
    item_list = deneme(item_list)  # too slow

    # sort to lowest to highest not working
    # x = np.array(item_list)
    # item_list = x[x[:, 1].argsort()]

    # sort to highest to lowest not working
    # x = np.array(item_list).reshape(int(len(item_list) / 3), 3)
    # x_sorted_asc = x[x[:, 1].argsort()[::-1]]

    print(item_list)
    return item_list


def move_to():  # do only one lunge
    i = 0
    ch_num = 0
    cell_list = get_cells()  # get the all numbers and positions

    while i < len(cell_list):
        chosen_cell = cell_list[i]
        for compared_cell in cell_list[i + 1:]:

            if chosen_cell[0] == compared_cell[0]:  # looking matching number
                if chosen_cell[1] == compared_cell[1]:  # looking x
                    if chosen_cell[2] > compared_cell[2]:
                        try:
                            driver.find_element(By.XPATH, '/html/body').send_keys(Keys.UP)
                            ch_num += 1
                            print("Up")
                        except StaleElementReferenceException:
                            print("Oops!")

                        return 0
                    elif chosen_cell[2] < compared_cell[2]:
                        try:
                            driver.find_element(By.XPATH, '/html/body').send_keys(Keys.DOWN)
                            ch_num += 1
                            print("Down")
                        except StaleElementReferenceException:
                            print("Oops!")

                        return 1

                if chosen_cell[2] == compared_cell[2]:  # looking y
                    if chosen_cell[1] > compared_cell[1]:
                        try:
                            driver.find_element(By.XPATH, '/html/body').send_keys(Keys.LEFT)
                            ch_num += 1
                            print("Left")
                        except StaleElementReferenceException:
                            print("Oops!")

                        return 2
                    elif chosen_cell[1] < compared_cell[1]:
                        try:
                            driver.find_element(By.XPATH, '/html/body').send_keys(Keys.RIGHT)
                            ch_num += 1
                            print("Right")
                        except StaleElementReferenceException:
                            print("Oops!")

                        return 3
        i += 1

        if ch_num == 0:  # if no-one math do random move
            driver.find_element(By.XPATH, '/html/body').send_keys(random.choice(MOVE))
            return -1


def go(url="https://play2048.co"):
    driver.get(url)  # go to webpage

    repeat_num = 0
    while 1:
        move_id = move_to()  # get the move way
        if move_id == move_to():  # checking the next move is same
            repeat_num += 1
            if repeat_num > 3:  # if it's get in infinite loop do random lunge to break the loop
                try:
                    driver.find_element(By.XPATH, '/html/body').send_keys(random.choice(MOVE))
                except StaleElementReferenceException:
                    print("Oops!")
        else:
            repeat_num = 0

        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/a[2]').click()
        except ElementNotInteractableException:
            pass

        time.sleep(WAIT_TIME)


go()  # magic is here
