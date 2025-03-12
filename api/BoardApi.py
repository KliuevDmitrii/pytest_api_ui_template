import requests
import json

class BoardApi:

    def __init__(self, base_url: str, api_key:str, token: str):
        self.base_url = base_url
        self.api_key = api_key
        self.token = token

    def get_all_boards_by_org_id(self, org_id: str) -> dict:
        path = f"{self.base_url}/organizations/{org_id}/boards"
        params = {
            "key": self.api_key,
            "token": self.token
    }

        resp = requests.get(path, params=params)

        print(f"Status Code: {resp.status_code}, Response Text: {resp.text}")

        try:
            return resp.json()
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON. Ответ API: {resp.text}")
    
    def create_board(self, org_id: str, name, default_lists = True):
        body = {
        "defaultLists": default_lists,
        "name": name,
        "token": self.token,
        "idOrganization": org_id }
        
        path = f"{self.base_url}/boards"
        params = {
            "key": self.api_key,
            "token":self.token
                  }

        resp = requests.post(path, json=body, params=params)

        return resp.json()
    
    def delete_board_by_id(self, board_id: str) -> dict:
        path = f"{self.base_url}/boards/{board_id}"
        params = {
            "key": self.api_key,
            "token":self.token
                  }

        resp = requests.delete(path, params=params)

        return resp.json()