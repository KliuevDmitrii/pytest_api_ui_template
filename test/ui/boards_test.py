import allure
import pytest
from faker import Faker

from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from pages.AuthPage import AuthPage
from pages.MainPage import MainPage

fake = Faker()

def add_new_board_test(browser, test_data: dict):
    username = test_data.get("username")
    email = test_data.get("email")
    password = test_data.get("pass")
    name_board = fake.word()

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)
    WebDriverWait(browser, 20).until(EC.url_contains("kliuev_dmitrii/boards"))

    main_page = MainPage(browser)
    main_page.click_button_create_board()
    main_page.add_name_board(name_board)
    main_page.click_button_create()
    main_page.click_button_boards()
    info = main_page.get_boards_info()

    with allure.step("Проверить, что создана доска с названием "+ name_board):
        assert info[0] == name_board
