""" __init__.py """

# Webserver
from flask import request
from flask import jsonify

# Models
from app.models import credentials
from app.models.human_resources import execute_query_users_get
from app.models.misc import execute_query_activity_log_post

# Utils
from app.utils.util import check_activity_log
from app.utils.util import insert_file_log
from app.utils.util import check_uuid
from app.utils.util import load_json

from app.utils.util import timer

key = load_json(file='./constants/key.json')['key']

@timer
def check_session(header={}):
    """ doctest for check_session (pendent try exception global of function) without unit test
    """
    function_response = {}
    function_response['status'] = False
    function_response['content'] = None
    validation = ''
    if 'User-Id' in header or 'Channel-Contact-Id' in header:
        if 'User-Id' in header:
            if isinstance(header['User-Id'], str):
                if check_uuid(header['User-Id']):
                    query_session = {"response_type": "table_data", "id": header['User-Id'], "search": '', "order_column_1": '', "order_direction_column_1": '', "limit": "5"}
                    execute_query_response = execute_query_users_get(query=query_session, credentials=credentials)
                    if execute_query_response['status']:
                        if len(execute_query_response['content']) == 1:
                            pass
                        else:
                            function_response['content'] = 'Not found user_id or duplicate'
                            validation += "False"
                    else:
                        function_response['content'] = 'Error in database connection'
                        validation += "False"
                else:
                    function_response['content'] = 'Incorret user_id format'
                    validation += "False"
            else:
                function_response['content'] = 'Incorret user_id type'
                validation += "False"
                
        if not validation:
            function_response['status'] = True
    else:
        function_response['content'] = 'not user_id and channel_contanct_id in header'
    
    return function_response

@timer
def insert_activity_log(input_function={}):
    """ insert_activity_log """
    function_response = {}
    function_response['status'] = False
    function_response['content'] = None
    #try:
    if True:
        check_activity_log_response = check_activity_log(input_function=input_function)
        if check_activity_log_response['status']:
            execute_query_response = execute_query_activity_log_post(query=input_function['activity_log'], credentials=credentials)
            if execute_query_response['status']:
                return function_response
            else:
                insert_file_log(function='execute_query_activity_log_post', \
                input_function=['input: ',input_function,'execute_query_activity_log_post: ',execute_query_response['content']])
        else:
            insert_file_log(function='insert_activity_log', \
                input_function=['input: ',input_function,'check_activity_log: ',check_activity_log_response['content']])
        return function_response
    #except Exception as error:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error : insert_activity_log', exc_type, fname, exc_tb.tb_lineno, str(error))
