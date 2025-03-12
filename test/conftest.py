# from logging import config
from socket import timeout
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from api.BoardApi import BoardApi
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.getint("ui", "timeout")

        try:
            browser_name = config.get("ui", "browser_name").lower()
        except KeyError:
            browser_name = "chrome"

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
def api_client() -> BoardApi:
    config = ConfigProvider()
    data_provider = DataProvider()
    return BoardApi(
        config.get("api", "base_url"),
        config.get("api", "api_key"),
        data_provider.get_token()
    )
    
@pytest.fixture
def api_client_no_auth() -> BoardApi:
    return BoardApi(ConfigProvider().get("api", "base_url"), "")

@pytest.fixture
def dummi_board_id() -> str:
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
        
@pytest.fixture
def test_data():
    return DataProvider()