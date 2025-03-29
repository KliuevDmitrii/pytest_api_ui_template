import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

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
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[data-testid='header-member-menu-button']"))
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
    def add_name_board(self, name_board: str):
        title_input = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                "input[data-testid='create-board-title-input']"))
            )
        title_input.send_keys(name_board)

    @allure.step("Нажать кнопку 'Создать'")
    def click_button_create(self):
        create_button = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                "button[data-testid='create-board-submit-button']"))
            )
        create_button.click()

    @allure.step("Нажать кнопку 'Доски' в меню")
    def click_button_boards(self):
        button_boards = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//p[@class='nNvJhnERHVQb9o' and text()='Доски']"))
            )
        button_boards.click()

    @allure.step("Получить список досок")
    def get_boards_info(self) -> list[str]:
        try:
            container = WebDriverWait(self.__driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.L0brLYR3ZZ6wm4"))
        )
            boards = container.find_elements(By.CSS_SELECTOR, "div.LinesEllipsis")
            return [board.text for board in boards]
        except TimeoutException:
            return []
    
    @allure.step("Открыть меню созданной доски")
    def click_menu_board(self):
        button_menu_board = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@aria-label='Меню']"))
            )
        button_menu_board.click()

    @allure.step("Выбрать 'Закрыть доску'")
    def click_closed_board(self):
        closed_board = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//div[contains(@class, 'S1YMKJFPn9WNGk') and text()='Закрыть доску']"))
            )
        closed_board.click()
        button_closed_board = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@data-testid='popover-close-board-confirm']"))
            )
        button_closed_board.click()

    @allure.step("Выбрать 'Удалить доску навсегда'")
    def click_delete_board(self):
        delete_board = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@data-testid='close-board-delete-board-button']"))
            )
        delete_board.click()
        button_delete_board = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@data-testid='close-board-delete-board-confirm-button']"))
            )
        button_delete_board.click()

    @allure.step("Нажать 'Добавить список'")
    def click_add_list(self):
        click_add_list = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@data-testid='list-composer-button']"
                ))
            )
        click_add_list.click()

    @allure.step("Добавить заголовок списка")
    def add_name_list(self, name_list: str):
        title_input = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                "//textarea[@data-testid='list-name-textarea']"
                ))
            )
        title_input.send_keys(name_list)

    @allure.step("Нажать кнопку 'Добавить список'")
    def click_button_add_list(self):
        click_button_add_list = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@data-testid='list-composer-add-list-button']"
                ))
            )
        click_button_add_list.click()
    
    @allure.step("Добавить заголовок карточки")
    def add_name_card(self, name_card: str):
        title_input = WebDriverWait(self.__driver, 15).until(
            EC.presence_of_element_located((By.XPATH, 
                "//textarea[@data-testid='list-card-composer-textarea']"
                ))
            )
        title_input.send_keys(name_card)

    @allure.step("Нажать кнопку 'Добавить карточку'")
    def click_button_add_card(self):
        button_add_card = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'SEj5vUdI3VvxDc') and @data-testid='list-card-composer-add-card-button']"
                ))
            )
        button_add_card.click()

    @allure.step("Закрыть добавление карточки")
    def click_close_card(self):
        close_card = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//span[@data-testid='CloseIcon']"
                ))
            )
        close_card.click()

    @allure.step("Проверка наличия карточки по названию")
    def check_card_by_name(self, name_card: str):
        try:
            element = WebDriverWait(self.__driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@data-testid='card-name' and text()='{name_card}']"))
            )
            print(f"Карточка с названием '{name_card}' найдена.")
            return True
        except:
            print(f"Карточка с названием '{name_card}' не найдена.")
            return False

    @allure.step("Нажать на карточку для редактирования")
    def click_edit_card(self):
        button_edit_card = WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//a[@data-testid='card-name']"
                ))
            )
        button_edit_card.click()

    @allure.step("Редактировать заголовок карточки")
    def edit_name_card(self, new_name_card: str):
        title_input = WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//textarea[@data-testid='card-back-title-input']"))
        )
        
        title_input.clear()
        title_input.send_keys(Keys.CONTROL + 'a')
        title_input.send_keys(Keys.DELETE)
        title_input.send_keys(new_name_card)
        
        WebDriverWait(self.__driver, 15).until(
            lambda d: title_input.get_attribute('value') == new_name_card
        )

    @allure.step("Нажать 'Сохранить' карточку")
    def click_save_card(self):
        save_card = WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@data-testid='description-save-button']"
                ))
            )
        save_card.click()