import json
from io import BytesIO
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestCategoryCrud():
    def test_sub_category_list(self, client, init_database):
        token = create_token()
        res = client.get('/category',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_category(self, client, init_database):
        token = create_token()
        res = client.get('/category/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_category_not_found(self, client, init_database):
        token = create_token()
        res = client.get('/category/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    
    def test_post_category(self, client, init_database):
        token = create_token()
        with open('/home/alta8/Downloads/standing.jpg', 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        res = client.post('/category',
                        content_type='multipart/form-data',
                        headers={'Authorization': 'Bearer ' + token},
                        data={'name':'tes',
                              'imgURL':(imgStringIO1, 'img1.jpg')
                            })
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_patch_category(self, client, init_database):
        token = create_token()
        data={
                "imgURL":"google.com",
                "name":"tes"
        }
        res = client.patch('/category/1',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_patch_category_not_found(self, client, init_database):
        token = create_token()
        data={
                "imgURL":"google.com",
                "name":"tes"
        }
        res = client.patch('/category/100',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_delete_category(self, client, init_database):
        token = create_token()
        res = client.delete('/category/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_category_not_found(self, client, init_database):
        token = create_token()
        res = client.delete('/category/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404