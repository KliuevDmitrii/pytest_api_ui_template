import requests
import json

class CardApi:
    def __init__(self, base_url: str, api_key: str, token: str):
        self.base_url = base_url
        self.api_key = api_key
        self.token = token

    def get_all_cards_by_list_id(self, list_id: str) -> list:
        """ Получить все карточки в списке """
        path = f"{self.base_url}/lists/{list_id}/cards"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        resp = requests.get(path, params=params)
        return self._handle_response(resp)

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