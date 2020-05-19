from flask_cors import CORS
from functools import wraps
from flask import Flask, request
import json, logging, config, os
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
# from werkzeug.contrib.cache import SimpleCache

# cache = SimpleCache()

app = Flask(__name__)

CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)

jwt = JWTManager(app)
if os.environ.get('FLASK_ENV', 'Production') == "Production":
    app.config.from_object(config.ProductionConfig)
elif os.environ.get('FLASK_ENV', 'Production') == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)


def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']:
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.before_request
def before_request():
    if request.method != 'OPTIONS':
        pass
    else :
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, PUT, GET, DELETE', 'Access-Control-Allow-Headers': '*'}

# add log method
@app.after_request
def after_request(response) :
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
            json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )
    else:
        app.logger.error("")
    
    return response

from blueprints.auth import bp_auth
app.register_blueprint(bp_auth, url_prefix='/auth')

from blueprints.client.resources import bp_client
app.register_blueprint(bp_client, url_prefix='/client')

db.create_all()