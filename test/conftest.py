from socket import timeout
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from api.BoardApi import BoardApi
from api.CardApi import CardApi
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

from faker import Faker

fake = Faker()

@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.getint("ui", "timeout")

        browser_name = config.get("ui", "browser_name", fallback="chrome")
        browser_name = browser_name.lower() if browser_name else "chrome"

        if browser_name == 'chrome':
            browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif browser_name in ['ff', 'firefox']:
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        else:
            raise ValueError(f"Неизвестное значение browser_name: {browser_name}")

        browser.implicitly_wait(timeout)
        browser.maximize_window()

    yield browser

    with allure.step("Закрыть браузер"):
            browser.quit()


@pytest.fixture
def board_api_client() -> BoardApi:
    with allure.step("Создать API-клиент для досок с авторизацией"):
        config = ConfigProvider()
        data_provider = DataProvider()
        return BoardApi(
            config.get("api", "base_url"),
            config.get("api", "api_key"),
            data_provider.get_token()
        )
    
@pytest.fixture
def card_api_client() -> CardApi:
    with allure.step("Создать API-клиент для карточек с авторизацией"):
        config = ConfigProvider()
        data_provider = DataProvider()
        return CardApi(
            config.get("api", "base_url"),
            config.get("api", "api_key"),
            data_provider.get_token()
        )

@pytest.fixture
def api_client_no_auth() -> BoardApi:
    with allure.step("Создать API-клиент без авторизации"):
        return BoardApi(ConfigProvider().get("api", "base_url"), "")

@pytest.fixture
def dummi_board_id() -> str:
    with allure.step("Создать временную доску для удаления"):
        api = BoardApi(
            ConfigProvider().get("api", "base_url"),
            DataProvider().get_token()
            )

        with allure.step("Предварительно создать доску"):
            board = api.create_board("Board to be deleted")
            if board and "id" in board:
                return board["id"]
            else:
                raise ValueError("Ошибка при создании доски: ответ API не содержит ID")
        
@pytest.fixture(scope="session")
def test_data():
    with allure.step("Загрузить тестовые данные"):
        return DataProvider()

@pytest.fixture
def board_id(board_api_client: BoardApi, test_data: DataProvider):
    with allure.step("Создать доску и вернуть её ID"):
        name_board = fake.company()
        org_id = test_data.get("org_id")
        board = board_api_client.create_board(org_id=org_id, name=name_board)
        assert board and "id" in board, "Ошибка при создании доски"
        return board["id"]

@pytest.fixture
def existing_board_id(board_api_client: BoardApi, test_data: DataProvider) -> str:
    with allure.step("Получить ID первой существующей доски в организации"):
        org_id = test_data.get("org_id")
        assert org_id, "Ошибка: отсутствует org_id в тестовых данных"

        boards = board_api_client.get_all_boards_by_org_id(org_id)
        assert boards, "Ошибка: в организации нет доступных досок"

        return boards[0]["id"]