""" logs.py """

# Other Libraries
import json
import datetime
import uuid

# Utils
from app.utils.util import formatter_datetime
from app.utils.util import check_field
from app.utils.util import insert_file_log

# Models
from app.models import credentials
from app.models.misc import execute_query_activity_log_post


def create_log(endpoint:str, table, headers, data, query, ip):
    
    method = endpoint.split("_")[-1]
    if method == 'get':
        activity_log = data[0][table]['id'] if len(data) == 1 and 'id' in query else None
    
    log = {}
    log['activity_log'] = {}
    log['activity_log']['id'] = str(uuid.uuid4()).upper()
    if 'User-Id' in headers:
        log['activity_log']['user_id_fk'] = headers['User-Id'] #*
    if 'Channel_Contact_Id' in headers:
        log['activity_log']['channel_contact_id_fk'] = headers['Channel-Contact-Id'] #*
    log['activity_log']['rel_id'] = activity_log if method == 'get' else query[table]['id']
    log['activity_log']['section'] = headers['Section']
    log['activity_log']['description'] = headers['Description']
    log['activity_log']['description_complement'] = headers['Description-Complement']
    log['activity_log']['complementary_information'] = headers['Complementary-Information']
    log['activity_log']['model'] = ''
    log['activity_log']['function'] = endpoint
    log['activity_log']['result'] = 'Success' #* response 200
    log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
    log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
    log['activity_log']['ip'] = ip #*
    log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
    insert_activity_log(input_function=log)

def check_activity_log(input_function={}):
    """ check_activity_log
    """
    function_response = {}
    function_response['status'] = False
    function_response['content'] = None
    input_validation_errors = ''
    query = {}
    query['activity_log'] = {}
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # id
    field = ['activity_log','id']
    check_field_result = check_field(input_function=input_function,field=field,type='uuid',default=str(uuid.uuid4()).upper(),optional=False)
    if check_field_result['status']:
        query['activity_log']['id'] = check_field_result['content']['activity_log']['id']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # user_id_fk
    field = ['activity_log','user_id_fk']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(45)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['user_id_fk'] = check_field_result['content']['activity_log']['user_id_fk']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # rel_id
    field = ['activity_log','rel_id']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(45)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['rel_id'] = check_field_result['content']['activity_log']['rel_id']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # section
    field = ['activity_log','section']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(45)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['section'] = check_field_result['content']['activity_log']['section']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # model
    field = ['activity_log','model']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(50)',default='',optional=False)
    if check_field_result['status']:
        query['activity_log']['model'] = check_field_result['content']['activity_log']['model']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # function
    field = ['activity_log','function']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(100)',default='',optional=False)
    if check_field_result['status']:
        query['activity_log']['function'] = check_field_result['content']['activity_log']['function']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # result
    field = ['activity_log','result']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(25)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['result'] = check_field_result['content']['activity_log']['result']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # description
    field = ['activity_log','description']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(16777215)',default='',optional=False)
    if check_field_result['status']:
        query['activity_log']['description'] = check_field_result['content']['activity_log']['description']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # description_complement
    field = ['activity_log','description_complement']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(16777215)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['description_complement'] = check_field_result['content']['activity_log']['description_complement']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # complementary_information
    field = ['activity_log','complementary_information']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(16777215)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['complementary_information'] = check_field_result['content']['activity_log']['complementary_information']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # json
    field = ['activity_log','response']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(16777215)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['response'] = check_field_result['content']['activity_log']['response']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # json
    field = ['activity_log','json']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(16777215)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['json'] = check_field_result['content']['activity_log']['json']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ip
    field = ['activity_log','ip']
    check_field_result = check_field(input_function=input_function,field=field,type='varchar(100)',default=None,optional=True)
    if check_field_result['status']:
        query['activity_log']['ip'] = check_field_result['content']['activity_log']['ip']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # added_on
    field = ['activity_log','added_on']
    check_field_result = check_field(input_function=input_function,field=field,type='timestamp',default=str(datetime.datetime.now()).split('.', maxsplit=1)[0],optional=False)
    if check_field_result['status']:
        query['activity_log']['added_on'] = check_field_result['content']['activity_log']['added_on']
    else:
        input_validation_errors += check_field_result['content']
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if not input_validation_errors:
        function_response['status'] = True
    else:
        function_response['content'] = input_validation_errors
    return function_response

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
