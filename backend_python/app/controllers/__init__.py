""" __init__.py """

# Models
from app.models import credentials
from app.models.human_resources import execute_query_users_get

# Utils
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
