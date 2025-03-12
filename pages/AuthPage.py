import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from configuration.ConfigProvider import ConfigProvider

class AuthPage:

    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url
        self.__driver = driver
    
    @allure.step("Перейти на страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)

    @allure.step("Авторизоваться под {email}:{password}")
    def login_as(self, email: str, password: str):
        self.__driver.find_element(By.CSS_SELECTOR, "#username").send_keys(email)
        self.__driver.find_element(By.CSS_SELECTOR, "#login-submit").click()
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "svg[role=presentation]")))
        self.__driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        self.__driver.find_element(By.CSS_SELECTOR, "#login-submit").click()

    def get_current_url(self):
        return self.__driver.current_url