import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

class MainPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        url = ConfigProvider().get("ui", "base_url")


    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.__driver.current_url
    
    @allure.step("Открыть боковое меню")
    def open_menu(self):
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='header-member-menu-button']"))
            ).click()

    @allure.step("Прочитать информацию о пользователе")    
    def get_account_info(self) -> list[str]:
        container = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.TyNFo3ay3iQKOz"))
        )
        name = container.find_element(By.CSS_SELECTOR, "div.lzFtVDCea8Z9jO").text
        email = container.find_element(By.CSS_SELECTOR, "div.Ej7WGzTnvdxL7I").text

        return [name, email]
    
    @allure.step("Нажать кнопку 'Создать доску'")
    def click_button_create_board(self):
        create_board_button = WebDriverWait(self.__driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Создать доску']"))
            )
        create_board_button.click()

    @allure.step("Добавить заголовок доски")
    def add_name_board(self, name_board):
        title_input = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='create-board-title-input']"))
            )
        title_input.send_keys(name_board)

    @allure.step("Нажать кнопку 'Создать'")
    def click_button_create(self):
        create_button = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='create-board-submit-button']"))
            )
        create_button.click()

    @allure.step("Нажать кнопку 'Доски' в меню")
    def click_button_boards(self):
        button_boards = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='nNvJhnERHVQb9o' and text()='Доски']"))
            )
        button_boards.click()

    @allure.step("Получить список досок")
    def get_boards_info(self) -> list[str]:
        container = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.L0brLYR3ZZ6wm4"))
            )
        boards = container.find_elements(By.CSS_SELECTOR, "div.LinesEllipsis")
        boards_names = [board.text for board in boards]
        return boards_names
