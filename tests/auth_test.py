import json
import os
import pytest
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestAuthCrud():
    @pytest.fixture
    def test_production(self):
        return os.environ.get('FLASK_ENV=Production')
        
    def test_post_auth_refresh_token(self, client, init_database):
            token = create_token()
            res = client.post('/auth/refresh',
                            headers={'Authorization': 'Bearer ' + token},
                            # query_string={'client_key':"internal", 'client_secret':"super_secret_client"},
                            content_type='application/json')
            
            res_json = json.loads(res.data)
            assert res.status_code == 200
    
    def test_get_auth(self, client, init_database):
            token = create_token()
            res = client.get('/auth',
                            headers={'Authorization': 'Bearer ' + token},
                            query_string={'username':"derby", 'password':"super_secret_client"},
                            content_type='application/json')
            
            res_json = json.loads(res.data)
            assert res.status_code == 401