import json
from io import BytesIO
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestProductCrud():
    def test_product_list(self, client, init_database):
        token = create_token()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_product(self, client, init_database):
        token = create_token()
        res = client.get('/product/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_product_not_found(self, client, init_database):
        token = create_token()
        res = client.get('/product/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    
    def test_post_product(self, client, init_database):
        token = create_token()
        with open('/home/alta8/Downloads/standing.jpg', 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        res = client.post('/product',
                        content_type='multipart/form-data',
                        headers={'Authorization': 'Bearer ' + token},
                        data={'name':'tes',
                              'price':100,
                              'stock':1,
                              'promo':"Yes",
                              'category_id':1,
                              'subcategory_id':1,
                              'url_image':(imgStringIO1, 'img1.jpg')
                            })
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_get_product_by_name(self, client, init_database):
        token = create_token()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'name':'makanan'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_product_by_price(self, client, init_database):
        token = create_token()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'price':10000},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_get_product_sort_desc_name(self, client, init_database):
        token = create_token()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'name', 'sort':'desc'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_product_sort_name(self, client, init_database):
        token = create_token()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'name'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_product_sort_desc_price(self, client, init_database):
        token = create_token()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'price', 'sort':'desc'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_product_sort_price(self, client, init_database):
        token = create_token()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'price'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200