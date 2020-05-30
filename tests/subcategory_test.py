import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestSubCategoryCrud():
    def test_sub_category_list(self, client, init_database):
        token = create_token()
        res = client.get('/subcategory',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_sub_category(self, client, init_database):
        token = create_token()
        res = client.get('/subcategory/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_sub_category_not_found(self, client, init_database):
        token = create_token()
        res = client.get('/subcategory/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    
    def test_post_sub_category(self, client, init_database):
        token = create_token()
        data={
                "category_id":1,
                "name":"sekarepmu"
        }
        res = client.post('/subcategory',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_patch_sub_category(self, client, init_database):
        token = create_token()
        data={
                "category_id":1,
                "name":"tes"
        }
        res = client.patch('/subcategory/1',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_patch_sub_category_not_found(self, client, init_database):
        token = create_token()
        data={
                "category_id":1,
                "name":"tes"
        }
        res = client.patch('/subcategory/100',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_delete_sub_category(self, client, init_database):
        token = create_token()
        res = client.delete('/subcategory/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_sub_category_not_found(self, client, init_database):
        token = create_token()
        res = client.delete('/subcategory/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404