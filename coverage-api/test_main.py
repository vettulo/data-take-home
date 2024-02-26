# from fastapi.testclient import TestClient
#
# from main import app
#
# client = TestClient(app)
# MEMBER_ID_ARG = 'member_id'
#
#
# def test_empty_request():
#     response = client.get('/')
#     assert response.status_code == 422
#     assert response.json() == {'detail': [{'loc': ['query', 'member_id'], 'msg': 'field required', 'type': 'value_error.missing'}]}
#
#
# def test_invalid_method():
#     response = client.post('/')
#     assert response.status_code == 405
#     response = client.patch('/')
#     assert response.status_code == 405
#     response = client.put('/')
#     assert response.status_code == 405
#     response = client.head('/')
#     assert response.status_code == 405
#     response = client.options('/')
#     assert response.status_code == 405
#
#
# def test_invalid_request_data():
#     response = client.get(f'/?{MEMBER_ID_ARG}=asd')
#     assert response.status_code == 422
#     assert response.json() == {'detail': [{'loc': ['query', 'member_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}
#
#
# def test_valid_request_data():
#     response = client.get(f'/?{MEMBER_ID_ARG}=1')
#     assert response.status_code == 200
#     assert response.json() == {'deductible': 1066, 'stop_loss': 11000, 'oop_max': 5666}
