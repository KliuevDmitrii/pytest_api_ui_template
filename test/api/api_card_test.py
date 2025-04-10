import allure
from api.CardApi import CardApi
from api.BoardApi import BoardApi
from faker import Faker

fake = Faker()

@allure.title("Создание новой карточки на доске")
def test_create_card(card_api_client: CardApi, board_id: str, test_data: dict, board_api_client: BoardApi):
    list_id = card_api_client.get_first_list_id(board_id)
    card_list_before = card_api_client.get_all_cards_by_list_id(list_id)
    
    name_card = fake.word()

    resp = card_api_client.create_card(list_id, name_card)  
    assert resp.get("id"), f"Ошибка: карта не была создана, ответ API: {resp}"

    card_list_after = card_api_client.get_all_cards_by_list_id(list_id)

    org_id = test_data.get("org_id")
    board_list_before = board_api_client.get_all_boards_by_org_id(org_id)
    board_id = board_list_before[0]["id"]

    board_api_client.delete_board_by_id(board_id)

    with allure.step("Проверить, что количество карточек увеличилось на одну"):
        assert len(card_list_after) - len(card_list_before) == 1

@allure.title("Редактирование карточки")
def test_update_card(card_api_client: CardApi, board_id: str, test_data: dict, board_api_client: BoardApi):
    list_id = card_api_client.get_first_list_id(board_id)

    original_name = fake.word()
    with allure.step(f"Создаем карточку с именем '{original_name}'"):
        create_response = card_api_client.create_card(list_id, original_name)
        card_id = create_response.get("id")
        assert card_id, f"Ошибка создания карточки: {create_response}"

    with allure.step("Проверяем исходное имя карточки"):
        card_data = card_api_client.get_card(card_id)
        assert card_data["name"] == original_name

    new_name = fake.word()
    with allure.step(f"Обновляем имя на '{new_name}'"):
        update_response = card_api_client.update_card(
            card_id=card_id,
            name=new_name
        )
        assert update_response["name"] == new_name

    with allure.step("Проверяем обновленное имя"):
        updated_card = card_api_client.get_card(card_id)
        assert updated_card["name"] == new_name
        assert updated_card["name"] != original_name

    test_data.get("org_id")
    board_api_client.delete_board_by_id(board_id)


@allure.title("Удаление карточки")
def test_delete_card(card_api_client: CardApi, temp_board_id):
    list_id = card_api_client.get_first_list_id(temp_board_id)

    with allure.step("Создать тестовую карточку"):
        original_name = fake.word()
        create_response = card_api_client.create_card(list_id, original_name)
        card_id = create_response.get("id")
        assert card_id, "Не удалось создать карточку"

    with allure.step("Получить список карточек до удаления"):
        card_list_before = card_api_client.get_all_cards_by_list_id(list_id)

    with allure.step(f"Удалить карточку с ID: {card_id}"):
        card_api_client.delete_card_by_id(card_id)

    with allure.step("Проверить, что количество карточек уменьшилось на одну"):
        card_list_after = card_api_client.get_all_cards_by_list_id(list_id)
        assert len(card_list_before) - len(card_list_after) == 1, "Ошибка: карточка не была удалена"








