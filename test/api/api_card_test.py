from api.CardApi import CardApi
from faker import Faker

fake = Faker()

def test_create_card(card_api_client: CardApi, board_id: str):
    list_id = card_api_client.get_first_list_id(board_id)
    card_list_before = card_api_client.get_all_cards_by_list_id(list_id)
    
    name_card = fake.word()

    resp = card_api_client.create_card(list_id, name_card)  
    assert resp.get("id"), f"Ошибка: карта не была создана, ответ API: {resp}"

    card_list_after = card_api_client.get_all_cards_by_list_id(list_id)

    assert len(card_list_after) - len(card_list_before) == 1

def test_delete_card(card_api_client: CardApi, existing_board_id: str):
    list_id = card_api_client.get_first_list_id(existing_board_id)
    card_list_before = card_api_client.get_all_cards_by_list_id(list_id)
    card_id = card_list_before[-1]["id"]
    resp = card_api_client.delete_card_by_id(card_id)
    print(f"Ответ API на удаление карточки: {resp}")

    card_list_after = card_api_client.get_all_cards_by_list_id(list_id)

    assert len(card_list_before) - len(card_list_after) == 1, "Ошибка: карточка не была удалена"






