""" app.py """

# Web Server
from flask import Flask
import flask.json as fj 

from app.controllers.human_resources import endpoint_users_get
from app.controllers.human_resources import endpoint_users_post
from app.controllers.human_resources import endpoint_users_patch
from app.controllers.human_resources import endpoint_genders_get
from app.controllers.human_resources import endpoint_genders_post
from app.controllers.human_resources import endpoint_genders_patch





#_____________________________________________________________________
import decimal

def run_app():
    """ run_app """
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = '2e117779-2cc4-42fe-b22b-5f6d63633b45'#'a3fd904d-09d1-4d2b-8940-c49104a2bb98'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    
    class MyJSONEncoder(fj.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, decimal.Decimal):
                # Convert decimal instances to strings.
                return str(obj)
            return super(MyJSONEncoder, self).default(obj)
    app.json_encoder = MyJSONEncoder
    #UPLOAD_FOLDER = './uploads'
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #https://flask.palletsprojects.com/en/2.0.x/api/#flask.Blueprint.add_url_rule
    
    app.add_url_rule("/users", methods=['GET'],   view_func=endpoint_users_get)
    app.add_url_rule("/users", methods=['POST'],  view_func=endpoint_users_post)
    app.add_url_rule("/users", methods=['PATCH'], view_func=endpoint_users_patch)
    app.add_url_rule("/genders", methods=['GET'],   view_func=endpoint_genders_get)
    app.add_url_rule("/genders", methods=['POST'],  view_func=endpoint_genders_post)
    app.add_url_rule("/genders", methods=['PATCH'], view_func=endpoint_genders_patch)











    app.run(host='0.0.0.0', port=80)