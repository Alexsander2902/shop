""" authentication.py """

# Other Libraries
import json
import datetime
import uuid
import copy
import random

# Webserver
from flask import request
from flask import jsonify

# Models
from app.models import credentials
from app.models.authentication import execute_query_authentication_post
from app.models.authentication import execute_query_user_auto_login_get
from app.models.authentication import execute_query_user_auto_login_post
from app.models.human_resources import execute_query_users_get

# Utils
from app.utils.util import generate_password
from app.utils.util import check_password
from app.utils.util import check_uuid
from app.utils.util import check_field
from app.utils.util import pathset
from app.utils.util import pathget
from app.utils.util import check_header
from app.utils.util import insert_file_log
from app.utils.util import formatter_datetime

# Controllers
from app.controllers import key
from app.controllers import check_session
from app.controllers.logs import insert_activity_log
from app.controllers.logs import create_log

def endpoint_authentication_post():
    """ doctest for endpoint_authentication_post (pendent try exception global of function) without unit test
    """
    endpoint_response = {}
    endpoint_response['status'] = False
    endpoint_response['content'] = None
    #try:
    if True:
        headers = dict(request.headers)
        log = {}
        log['activity_log'] = {}
        log['activity_log']['id'] = str(uuid.uuid4()).upper()
        log['activity_log']['user_id_fk'] = None #*
        log['activity_log']['model'] = ''
        log['activity_log']['function'] = 'endpoint_authentication_post'
        log['activity_log']['ip'] = request.remote_addr #*
        log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
        check_header_response = check_header(header=headers,key=key)
        if check_header_response['status']:
            log['activity_log']['section'] = headers['Section']
            log['activity_log']['description'] = headers['Description']
            log['activity_log']['description_complement'] = headers['Description-Complement']
            log['activity_log']['complementary_information'] = headers['Complementary-Information']
            request_json = request.get_json()
            #print('pre request_json',json.dumps(request_json,indent=4))
            input_validation_errors = ''
            query = {}
            query['user'] = {}
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            field = ['user','login']
            check_field_result = check_field(input_function=request_json,field=field,type='login',default='',optional=False)
            if check_field_result['status']:
                pathset(query, field, pathget(check_field_result['content'], field)['content'])
            else:
                input_validation_errors += check_field_result['content']
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            field = ['user','password']
            check_field_result = check_field(input_function=request_json,field=field,type='password',default='',optional=False)
            if check_field_result['status']:
                pathset(query, field, pathget(check_field_result['content'], field)['content'])
            else:
                input_validation_errors += check_field_result['content']
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            field = ['user','autologin']
            check_field_result = check_field(input_function=request_json,field=field,type='boolean',default=False,optional=True)
            if check_field_result['status']:
                pathset(query, field, pathget(check_field_result['content'], field)['content'])
            else:
                input_validation_errors += check_field_result['content']
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            if not input_validation_errors:
                #print('pos request_json',json.dumps(query,indent=4))
                execute_query_response = execute_query_authentication_post(query=query['user'], credentials=credentials)
                if execute_query_response['status']:
                    if len(execute_query_response['content']) == 1:
                        if check_password(query['user']['password'], execute_query_response['content'][0]['user']['password']):
                            data = execute_query_response['content'][0]
                            if query['user']['autologin']:
                                temp_query = {
                                    "id" : str(uuid.uuid4()).upper(),
                                    "user_id_fk" : execute_query_response['content'][0]['user']['id'],
                                    "user_hash" : str(generate_password(str(random.randint(0,1024)))).split("'")[1],
                                    "added_on" : str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                                }
                                execute_query_response3 = execute_query_user_auto_login_post(query=temp_query, credentials=credentials)
                                if execute_query_response3['status']:
                                    data['user_auto_login'] = temp_query
                                    log['activity_log']['rel_id'] = execute_query_response['content'][0]['user']['id']
                                    log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                                    log['activity_log']['result'] = 'Success' #* response
                                    log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                                    insert_activity_log(input_function=log)
                                    return jsonify(data), 200
                                else:
                                    data = {'message': '500 Internal Server Error - Error in connection or insert'}
                                    log['activity_log']['rel_id'] = execute_query_response['content'][0]['user']['id']
                                    log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                                    log['activity_log']['result'] = 'Failed' #* response
                                    query['user']['password'] = str(query['user']['password'])
                                    log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                                    insert_activity_log(input_function=log)
                                    return jsonify(data), 500
                            else:
                                log['activity_log']['rel_id'] = execute_query_response['content'][0]['user']['id']
                                log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                                log['activity_log']['result'] = 'Success' #* response
                                log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                                insert_activity_log(input_function=log)
                                return jsonify(data), 200
                        else:
                            data = {'message': '500 Internal Server Error - Wrong password'}
                            log['activity_log']['rel_id'] = execute_query_response['content'][0]['user']['id']
                            log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                            log['activity_log']['result'] = 'Failed' #* response
                            query['user']['password'] = str(query['user']['password'])
                            log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                            insert_activity_log(input_function=log)
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Login not found or duplicated'}
                        insert_file_log(function='endpoint_authentication_post', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    data = {'message': '500 Internal Server Error - Error in connection or insert'}
                    insert_file_log(function='endpoint_authentication_post', \
                        input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                    return jsonify(data), 500
            else:
                insert_file_log(function='endpoint_authentication_post', \
                    input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
        else:
            insert_file_log(function='endpoint_authentication_post', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_authentication_post: ', exc_type, fname, exc_tb.tb_lineno, str(e))

#query com 1 o mais recente pro authentication ???????
def endpoint_user_auto_login_get():
    """ doctest for endpoint_user_auto_login_get (pendent try exception global of function) without unit test
    """
    endpoint_response = {}
    endpoint_response['status'] = False
    endpoint_response['content'] = None
    #try:
    if True:
        headers = dict(request.headers)
        check_header_response = check_header(header=headers,key=key)
        if check_header_response['status']:
            check_session_response = check_session(header=headers)
            if check_session_response['status']:
                input_validation_errors = not check_uuid(request.args.get('user_id_fk'))
                query = {"user_id_fk": request.args.get('user_id_fk'), "user_hash": request.args.get('user_hash')}
                if not input_validation_errors and request.args.get('user_id_fk') and request.args.get('user_hash'):
                    execute_query_response2 = execute_query_users_get(query={'id': request.args.get('user_id_fk')}, credentials=credentials)
                    if execute_query_response2['status']:
                        if len(execute_query_response2['content']) == 1:
                            execute_query_response3 = execute_query_authentication_post(query={'login': execute_query_response2['content'][0]['user']['login']}, credentials=credentials)
                            if execute_query_response3['status']:
                                if len(execute_query_response3['content']) == 1:
                                    execute_query_response = execute_query_user_auto_login_get(query=query, credentials=credentials)
                                    if execute_query_response['status']:
                                        if (len(execute_query_response['content']) == 1):
                                            
                                            data = execute_query_response3['content'][0]
                                            data['user_auto_login'] = execute_query_response['content'][0]['user_auto_login']
                                            create_log('endpoint_user_auto_login_get', 'user_auto_login', headers, data, query, ip= request.remote_addr)
                                            return jsonify(data), 200
                                        
                                        else:
                                            data = {'message': '500 Internal Server Error - Forbidden'}
                                            insert_file_log(function='endpoint_user_auto_login_get', \
                                                input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                                            return jsonify(data), 500
                                    else:
                                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                                        insert_file_log(function='endpoint_user_auto_login_get', \
                                            input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                                        return jsonify(data), 500
                                else:
                                    data = {'message': '500 Internal Server Error - login Not found'}
                                    insert_file_log(function='endpoint_user_auto_login_get', \
                                        input_function=['query: ',query,'execute_query_response: ',execute_query_response3['content']])
                                    return jsonify(data), 500
                            else:
                                data = {'message': '500 Internal Server Error - Error in connection or insert'}
                                insert_file_log(function='endpoint_user_auto_login_get', \
                                    input_function=['query: ',query,'execute_query_response: ',execute_query_response3['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - user_id_fk Not found'}
                            insert_file_log(function='endpoint_user_auto_login_get', \
                                input_function=['query: ',query,'execute_query_response: ',execute_query_response2['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_user_auto_login_get', \
                            input_function=['query: ',query,'execute_query_response: ',execute_query_response2['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_user_auto_login_get', \
                        input_function=['query: ',query,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+str(input_validation_errors)+")"}), 500
            else:
                insert_file_log(function='endpoint_user_auto_login_get', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_user_auto_login_get', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_user_auto_login_get: ', exc_type, fname, exc_tb.tb_lineno, str(e))
