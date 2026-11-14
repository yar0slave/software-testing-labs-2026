import os
import pytest
import requests
BASE = os.getenv('API_BASE_URL', 'https://jsonplaceholder.typicode.com')
@pytest.mark.parametrize('method,path,payload,status', [
    ('GET','/users/1',None,200),
    ('POST','/users',{'name':'Test Student','username':'student','email':'student@example.com'},201),
    ('PUT','/users/1',{'name':'Updated Student','username':'student','email':'updated@example.com'},200),
])
def test_users(method, path, payload, status):
    response = requests.request(method, BASE+path, json=payload, timeout=20)
    assert response.status_code == status
    assert 'application/json' in response.headers['Content-Type']
    body = response.json()
    assert isinstance(body,dict)
    assert isinstance(body['id'],int)
    for key in ('name','username','email'):
        assert isinstance(body[key],str)
    if payload:
        for key,value in payload.items():
            assert body[key] == value
        assert body['id'] == (11 if method == 'POST' else 1)
    else:
        assert body['id'] == 1
        assert body['username'] == 'Bret'
        assert body['email'] == 'Sincere@april.biz'
