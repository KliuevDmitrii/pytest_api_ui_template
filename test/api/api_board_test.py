from api.BoardApi import BoardApi
from faker import Faker

fake = Faker()

def test_create_board(board_api_client: BoardApi, test_data: dict):
    org_id = test_data.get("org_id")
    board_list_before = board_api_client.get_all_boards_by_org_id(org_id)

    name_board = fake.word()
    resp = board_api_client.create_board(org_id, name_board)
    board_list_after = board_api_client.get_all_boards_by_org_id(org_id)

    assert len(board_list_after) - len(board_list_before) == 1

def test_delete_board(board_api_client: BoardApi, test_data: dict):
    org_id = test_data.get("org_id")
    board_list_before = board_api_client.get_all_boards_by_org_id(org_id)
    board_id = board_list_before[0]["id"]

    resp = board_api_client.delete_board_by_id(board_id)
    print(resp)

    board_list_after = board_api_client.get_all_boards_by_org_id(org_id)

    assert len(board_list_before) - len(board_list_after) == 1
