import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestClientCrud():
    def test_client_list(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_client_list_non_auth(self, client, init_database):
        token = create_token_non_internal()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 403
    
    def test_client(self, client, init_database):
        token = create_token()
        res = client.get('/client/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_not_found(self, client, init_database):
        token = create_token()
        res = client.get('/client/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    
    def test_post_client(self, client, init_database):
        token = create_token()
        data={
                "username":"bebas aja",
                "password":"sekarepmu"
        }
        res = client.post('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_patch_client(self, client, init_database):
        token = create_token()
        data={
                "username":"tes",
                "password":"tes"
        }
        res = client.patch('/client/1',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_patch_client_not_found(self, client, init_database):
        token = create_token()
        data={
                "username":"tes",
                "password":"tes"
        }
        res = client.patch('/client/100',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_delete_client(self, client, init_database):
        token = create_token()
        res = client.delete('/client/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_client_not_found(self, client, init_database):
        token = create_token()
        res = client.delete('/client/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404