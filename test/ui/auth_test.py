import allure
import pytest

from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from pages.AuthPage import AuthPage
from pages.MainPage import MainPage


def auth_test(browser, test_data: dict):
    username = test_data.get("username")
    email = test_data.get("email")
    password = test_data.get("pass")

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)
    WebDriverWait(browser, 20).until(EC.url_contains("kliuev_dmitrii/boards"))

    main_page = MainPage(browser)
    main_page.open_menu()
    info = main_page.get_account_info()
    
    current_url = main_page.get_current_url()
    with allure.step("Проверить, что URL " + current_url + "заканчивается на kliuev_dmitrii/boards"):
        assert main_page.get_current_url().endswith("kliuev_dmitrii/boards")
    
    with allure.step("Проверить, что указаны данные пользователя"):
        with allure.step("Имя пользователя должно быть "+username):
             assert info[0] == username
             
        with allure.step("Почта пользователя должна быть "+email):   
             assert info[1] == email
