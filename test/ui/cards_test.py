import allure
import pytest
from faker import Faker

from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.AuthPage import AuthPage
from pages.MainPage import MainPage

fake = Faker()

@allure.title("Добавление новой карточки на доску")
def add_new_card_test(browser, test_data: dict):
    username = test_data.get("username")
    email = test_data.get("email")
    password = test_data.get("pass")

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)

    main_page = MainPage(browser)
    main_page.click_button_create_board()

    name_board = fake.word()

    main_page.add_name_board(name_board)
    main_page.click_button_create()

    name_card = fake.state()

    main_page.add_name_card(name_card)
    main_page.click_button_add_card()
    main_page.click_close_card()

    with allure.step(f"Проверка наличия карточки с названием: {name_card}"):
        assert main_page.check_card_by_name(name_card) == True, f"Карточка с названием '{name_card}' не найдена."

@allure.title("Редактирование новой карточки")
def edit_card_test(browser, test_data: dict):
    username = test_data.get("username")
    email = test_data.get("email")
    password = test_data.get("pass")

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)

    main_page = MainPage(browser)
    main_page.click_button_create_board()

    name_board = fake.word()

    main_page.add_name_board(name_board)
    main_page.click_button_create()

    name_card = fake.word()

    main_page.add_name_card(name_card)
    main_page.click_button_add_card()
    main_page.click_close_card()
    main_page.click_card(name_card)
    
    new_name = fake.word()

    main_page.edit_name_card(new_name)
    main_page.click_save_card()
    main_page.click_close_card()

    with allure.step(f"Проверка наличия карточки с новым названием: {new_name}"):
        assert main_page.check_card_by_name(new_name) == True, f"Карточка с новым названием '{new_name}' не найдена."

@allure.title("Перетаскивание карточки в другой список")
def drag_and_drop_card_test(browser, test_data: dict):
    username = test_data.get("username")
    email = test_data.get("email")
    password = test_data.get("pass")

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)

    main_page = MainPage(browser)
    main_page.click_button_create_board()

    name_board = fake.word()

    main_page.add_name_board(name_board)
    main_page.click_button_create()

    card_name = fake.word()

    main_page.add_name_card(card_name)
    main_page.click_button_add_card()
    main_page.click_close_card()
    main_page.drag_and_drop_card(card_name)

    with allure.step("Проверка, что карточка перемещена в 'В процессе'"):
        assert main_page.is_card_in_list(card_name), "Карточка не переместилась в список 'В процессе'" 

@allure.title("Архивация новой карточки")
def archive_card_test(browser, test_data: dict):
    username = test_data.get("username")
    email = test_data.get("email")
    password = test_data.get("pass")

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)

    main_page = MainPage(browser)
    main_page.click_button_create_board()

    name_board = fake.word()

    main_page.add_name_board(name_board)
    main_page.click_button_create()

    name_card = fake.word()

    main_page.add_name_card(name_card)
    main_page.click_button_add_card()
    main_page.click_close_card()
    main_page.click_card(name_card)
    main_page.click_archive_card()
    main_page.click_close_card()

    with allure.step(f"Проверка наличия карточки : {name_card}"):
        assert main_page.check_card_by_name(name_card) == False, f"Карточка с названием '{name_card}' найдена."