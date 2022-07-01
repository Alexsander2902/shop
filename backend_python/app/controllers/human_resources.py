""" human_resources.py """

# Other Libraries
import json
import datetime
import uuid
import copy

# Webserver
from flask import request
from flask import jsonify

# Models
from app.models import credentials
from app.models.authentication import execute_query_authentication_post
from app.models.human_resources import execute_query_genders_get
from app.models.human_resources import execute_query_genders_post
from app.models.human_resources import execute_query_genders_patch
from app.models.human_resources import execute_query_users_get
from app.models.human_resources import execute_query_users_post
from app.models.human_resources import execute_query_users_patch


from app.models import execute_query_get_max_order

# Utils
from app.utils.util import check_uuid
from app.utils.util import check_field
from app.utils.util import pathget
from app.utils.util import pathset
from app.utils.util import check_header
from app.utils.util import insert_file_log
from app.utils.util import generate_password

# Controllers
from app.controllers import key
from app.controllers import check_session
from app.controllers.logs import create_log


def endpoint_genders_get():
    """ doctest for endpoint_genders_get (pendent try exception global of function) without unit test
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
                input_validation_errors = not check_uuid(request.args.get('id'))
                query = {"response_type": request.args.get('response_type'), "id": request.args.get('id'), "search": request.args.get('search'), "order_column_1": request.args.get('order_column_1'), "order_direction_column_1": request.args.get('order_direction_column_1'), "limit": request.args.get('limit')}
                if not input_validation_errors:
                    execute_query_response = execute_query_genders_get(query=query, credentials=credentials)
                    if execute_query_response['status']:
                        if execute_query_response['content'] or not request.args.get('id'):
                            if (len(execute_query_response['content']) == 1 and request.args.get('id')) or \
                                (len(execute_query_response['content']) >= 0 and not request.args.get('id')):
                                    
                                data = execute_query_response['content']
                                create_log('endpoint_genders_get', 'gender', headers, data, query, ip= request.remote_addr)
                                return jsonify(data), 200
                            
                            else:
                                data = {'message': '500 Internal Server Error - Not found uniq'}
                                insert_file_log(function='endpoint_genders_get', \
                                    input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - Not found'}
                            insert_file_log(function='endpoint_genders_get', \
                                input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_genders_get', \
                            input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_genders_get', \
                        input_function=['query: ',query,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+str(input_validation_errors)+")"}), 500
            else:
                insert_file_log(function='endpoint_genders_get', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_genders_get', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_genders_get: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_genders_post():
    """ doctest for endpoint_genders_post (pendent try exception global of function) without unit test
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
                request_json = request.get_json()
                #print('pre request_json',json.dumps(request_json,indent=4))
                input_validation_errors = ''
                # SQL Reference: VALUES('', 2, '', '', '', NULL, NULL, NULL, NULL, NULL, 1, current_timestamp());
                query = {}
                query['gender'] = {}
                query['gender']['id'] = str(uuid.uuid4()).upper()
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['gender','id']
                check_field_result = check_field(input_function=copy.deepcopy(query),field=field,type='uuid',default=str(uuid.uuid4()).upper(),optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['gender','name']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(25)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                execute_pre_query_response = execute_query_get_max_order(table='gender')
                if execute_pre_query_response['status']:
                    query['gender']['order'] = execute_pre_query_response['content'][0]['gender']['order']
                else:
                    input_validation_errors += 'order not found'
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['gender','active']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=1,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                query['gender']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                #field = ['gender','added_on']
                #check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='timestamp',default=str(datetime.datetime.now()).split('.', maxsplit=1)[0],optional=False)
                #if check_field_result['status']:
                #    query = check_field_result['content']
                #else:
                #    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4))
                    execute_query_response = execute_query_genders_post(query=query['gender'], credentials=credentials)
                    if execute_query_response['status']:
                        
                        data = {'gender': {'id': query['gender']['id']}}
                        create_log('endpoint_genders_post', 'gender', headers, data, query, ip= request.remote_addr)
                        return jsonify(data), 200
                    
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_genders_post', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_genders_post', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_genders_post', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_genders_post', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_genders_post: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_genders_patch():
    """ doctest for endpoint_genders_patch (pendent try exception global of function) without unit test
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
                request_json = request.get_json()
                #print('pre request_json',json.dumps(request_json,indent=4))
                input_validation_errors = ''
                # SQL Reference: VALUES('', 2, '', '', '', NULL, NULL, NULL, NULL, NULL, 1, current_timestamp());
                query = {}
                query['gender'] = {}
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['gender','id']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='uuid',default=2,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['gender','name']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(25)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['gender','active']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=1,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['gender','excluded']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=0,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4))
                    execute_query_response = execute_query_genders_patch(query=query['gender'], credentials=credentials)
                    if execute_query_response['status']:
                        
                        data = {'gender': {'id': query['gender']['id']}}
                        create_log('endpoint_genders_patch', 'gender', headers, data, query, ip= request.remote_addr)
                        return jsonify(data), 200
                    
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_genders_patch', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_genders_patch', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_genders_patch', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_genders_patch', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_genders_patch: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_users_get():
    """ doctest for endpoint_users_get (pendent try exception global of function) without unit test
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
                input_validation_errors = not check_uuid(request.args.get('id'))
                query = {"response_type": request.args.get('response_type'), "id": request.args.get('id'), "search": request.args.get('search'), "order_column_1": request.args.get('order_column_1'), "order_direction_column_1": request.args.get('order_direction_column_1'), "limit": request.args.get('limit')}
                if not input_validation_errors:
                    execute_query_response = execute_query_users_get(query=query, credentials=credentials)
                    if execute_query_response['status']:
                        if execute_query_response['content'] or not request.args.get('id'):
                            if (len(execute_query_response['content']) == 1 and request.args.get('id')) or \
                                (len(execute_query_response['content']) >= 0 and not request.args.get('id')):
                                                                                  
                                data = execute_query_response['content']
                                create_log('endpoint_users_get', 'user', headers, data, query, ip= request.remote_addr)
                                return jsonify(data), 200
                            
                            else:
                                data = {'message': '500 Internal Server Error - Not found uniq'}
                                insert_file_log(function='endpoint_users_get', \
                                    input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - Not found'}
                            insert_file_log(function='endpoint_users_get', \
                                input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_users_get', \
                            input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_users_get', \
                        input_function=['query: ',query,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+str(input_validation_errors)+")"}), 500
            else:
                insert_file_log(function='endpoint_users_get', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_users_get', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_users_get: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_users_post():
    """ doctest for endpoint_users_post (pendent try exception global of function) without unit test
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
                request_json = request.get_json()
                #print('pre request_json',json.dumps(request_json,indent=4,default=formatter_datetime))
                input_validation_errors = ''
                # SQL Reference: VALUES('', '', '', '', '', 25, 1, current_timestamp());
                query = {}
                query['user'] = {}
                query['user']['id'] = str(uuid.uuid4()).upper()
                query['user']['user_preferences_id_fk'] = str(uuid.uuid4()).upper()
                query['user']['user_history_id'] = str(uuid.uuid4()).upper()
                query['user']['user_headers'] = headers['User-Id']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','id']
                check_field_result = check_field(input_function=copy.deepcopy(query),field=field,type='uuid',default=str(uuid.uuid4()).upper(),optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','admin']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=0,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','individual_id_fk']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='uuid',default=str(uuid.uuid4()).upper(),optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','alias']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(25)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','login']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='login',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','password']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='password',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                    query['user']['password'] = generate_password(query['user']['password'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','pagination']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='int(11)',default=25,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','active']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=1,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                query['user']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4,default=formatter_datetime))
                    execute_query_response = execute_query_authentication_post(query=query['user'], credentials=credentials)
                    if execute_query_response['status']:
                        if len(execute_query_response['content']) == 0:
                            execute_query_response2 = execute_query_users_post(query=query['user'], credentials=credentials)
                            if execute_query_response2['status']:
                                
                                data = {'user': {'id': query['user']['id']}}
                                create_log('endpoint_genders_get', 'gender', headers, data, query, ip= request.remote_addr)
                                return jsonify(data), 200
                            
                            else:
                                data = {'message': '500 Internal Server Error - Error in connection or insert'}
                                insert_file_log(function='endpoint_users_post', \
                                    input_function=['request_json: ',request_json,'execute_query_response2: ',execute_query_response2['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - Login already in use'} #Login not found or duplicated
                            insert_file_log(function='endpoint_users_post', \
                                input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_users_post', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_users_post', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_users_post', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_users_post', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_users_post: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_users_patch():
    """ doctest for endpoint_users_patch (pendent try exception global of function) without unit test
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
                request_json = request.get_json()
                #print('pre request_json',json.dumps(request_json,indent=4))
                input_validation_errors = ''
                # SQL Reference: VALUES('', '', '', '', '', 25, 1, current_timestamp());
                query = {}
                query['user'] = {}
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','id']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='uuid',default=2,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','admin']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=0,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','individual_id_fk']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(45)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','alias']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(25)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','login']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='login',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','password']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='password',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                    query['user']['password'] = str(generate_password(query['user']['password'])).split("'")[1]
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','pagination']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='int(11)',default=25,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','active']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=1,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['user','excluded']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=0,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4))
                    execute_query_response = execute_query_authentication_post(query=query['user'], credentials=credentials)
                    if execute_query_response['status']:
                        if len(execute_query_response['content']) == 1:
                            execute_query_response2 = execute_query_users_patch(query=query['user'], credentials=credentials)
                            if execute_query_response2['status']:
                                
                                data = {'user': {'id': query['user']['id']}}
                                create_log('endpoint_users_get', 'user', headers, data, query, ip= request.remote_addr)
                                return jsonify(data), 200
                            
                            else:
                                data = {'message': '500 Internal Server Error - Error in connection or insert'}
                                insert_file_log(function='endpoint_users_put', \
                                    input_function=['request_json: ',request_json,'execute_query_response2: ',execute_query_response2['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - Login not found or duplicated'}
                            insert_file_log(function='endpoint_users_put', \
                                input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_users_patch', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_users_patch', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_users_patch', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_users_patch', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_users_patch: ', exc_type, fname, exc_tb.tb_lineno, str(e))
