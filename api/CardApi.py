import allure
import requests
import json

class CardApi:
    """ Этот класс предназначен для работы с API создания карточек """
    def __init__(self, base_url: str, api_key: str, token: str):
        self.base_url = base_url
        self.api_key = api_key
        self.token = token

    @allure.step("Получить все карточки в списке")
    def get_all_cards_by_list_id(self, list_id: str) -> list:
        """ Получить все карточки в списке """
        path = f"{self.base_url}/lists/{list_id}/cards"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        resp = requests.get(path, params=params)
        return self._handle_response(resp)
    
    @allure.step("Получить информацию о конкретной карточке")
    def get_card(self, card_id: str) -> dict:
        """Получить информацию о конкретной карточке"""
        path = f"{self.base_url}/cards/{card_id}"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        response = requests.get(path, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Ошибка получения карточки {card_id}: {response.status_code}")
        
        return response.json()

    @allure.step("Получить ID первого списка на доске")
    def get_first_list_id(self, board_id: str) -> str:
        """ Получить ID первого списка на доске """
        path = f"{self.base_url}/boards/{board_id}/lists"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        resp = requests.get(path, params=params)
        lists = self._handle_response(resp)
        if not lists:
            raise ValueError(f"Ошибка: на доске {board_id} нет списков")
        return lists[0]["id"]

    @allure.step("Создать новую карточку в списке")
    def create_card(self, list_id: str, name: str) -> dict:
        """ Создать новую карточку в списке """
        path = f"{self.base_url}/cards"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        body = {
            "idList": list_id,
            "name": name
        }
        resp = requests.post(path, json=body, params=params)
        return self._handle_response(resp)
    
    @allure.step("Редактировать карточку в списке")
    def update_card(self, card_id: str, name: str) -> dict:
        """ Редактировать карточку по ID """
        path = f"{self.base_url}/cards/{card_id}"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        data = {
            "name": name
        }
        resp = requests.put(path, params=params, json=data)
        return self._handle_response(resp)

    @allure.step("Удалить карточку по ID")
    def delete_card_by_id(self, card_id: str) -> dict:
        """ Удалить карточку по ID """
        path = f"{self.base_url}/cards/{card_id}"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        resp = requests.delete(path, params=params)
        return self._handle_response(resp)
    
    def _handle_response(self, resp):
        """ Вспомогательный метод для обработки ответа """
        try:
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Ошибка API: {e}, ответ: {resp.text}")
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON: {resp.text}")