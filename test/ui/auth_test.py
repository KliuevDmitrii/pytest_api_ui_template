import allure
import pytest

from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from pages.AuthPage import AuthPage
from pages.MainPage import MainPage

@allure.title("Авторизация пользователя")
def auth_test(browser, test_data: dict):
    username = test_data.get("username")
    email = test_data.get("email")
    password = test_data.get("pass")

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)

    main_page = MainPage(browser)
    main_page.open_menu()
    info = main_page.get_account_info()
    
    current_url = main_page.get_current_url()
    with allure.step("Проверить, что URL " + current_url + "заканчивается на boards"):
        assert main_page.get_current_url().endswith("boards")
    
    with allure.step("Проверить, что указаны данные пользователя"):
        with allure.step("Имя пользователя должно быть "+username):
             assert info[0] == username
             
        with allure.step("Почта пользователя должна быть "+email):   
             assert info[1] == email
