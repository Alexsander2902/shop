""" email.py """

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
from app.models.email import execute_query_email_queues_get
from app.models.email import execute_query_email_queues_post
from app.models.email import execute_query_email_queues_patch
from app.models.email import execute_query_email_templates_get
from app.models.email import execute_query_email_templates_post
from app.models.email import execute_query_email_templates_patch

# Utils
from app.utils.util import check_uuid
from app.utils.util import check_field
from app.utils.util import pathget
from app.utils.util import pathset
from app.utils.util import check_header
from app.utils.util import insert_file_log
from app.utils.util import formatter_datetime
from app.utils.util import load_file

from app.utils.gmail import send_email
gmail_credentials = json.loads(load_file(file='./constants/gmail.json'))

# Controllers
from app.controllers import key
from app.controllers import check_session
from app.controllers import insert_activity_log


def endpoint_email_queues_get():
    """ doctest for endpoint_email_queues_get (pendent try exception global of function) without unit test
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
                    execute_query_response = execute_query_email_queues_get(query=query, credentials=credentials)
                    if execute_query_response['status']:
                        if execute_query_response['content'] or not request.args.get('id'):
                            if (len(execute_query_response['content']) == 1 and request.args.get('id')) or \
                                (len(execute_query_response['content']) >= 0 and not request.args.get('id')):
                                data = execute_query_response['content']
                                log = {}
                                log['activity_log'] = {}
                                log['activity_log']['id'] = str(uuid.uuid4()).upper()
                                if 'User-Id' in headers:
                                    log['activity_log']['user_id_fk'] = headers['User-Id'] #*
                                if 'Channel_Contact_Id' in headers:
                                    log['activity_log']['channel_contact_id_fk'] = headers['Channel-Contact-Id'] #*
                                log['activity_log']['rel_id'] = None #*
                                if (len(execute_query_response['content']) == 1 and request.args.get('id')):
                                    log['activity_log']['rel_id'] = execute_query_response['content'][0]['email_queue']['id']
                                log['activity_log']['section'] = headers['Section']
                                log['activity_log']['description'] = headers['Description']
                                log['activity_log']['description_complement'] = headers['Description-Complement']
                                log['activity_log']['complementary_information'] = headers['Complementary-Information']
                                log['activity_log']['model'] = ''
                                log['activity_log']['function'] = 'endpoint_email_queues_get'
                                log['activity_log']['result'] = 'Success' #* response
                                log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                                log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                                log['activity_log']['ip'] = request.remote_addr #*
                                log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                                insert_activity_log(input_function=log)
                                return jsonify(data), 200
                            else:
                                data = {'message': '500 Internal Server Error - Not found uniq'}
                                insert_file_log(function='endpoint_email_queues_get', \
                                    input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - Not found'}
                            insert_file_log(function='endpoint_email_queues_get', \
                                input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_email_queues_get', \
                            input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_email_queues_get', \
                        input_function=['query: ',query,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+str(input_validation_errors)+")"}), 500
            else:
                insert_file_log(function='endpoint_email_queues_get', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_email_queues_get', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_email_queues_get: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_email_queues_post():
    """ doctest for endpoint_email_queues_post (pendent try exception global of function) without unit test
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
                # SQL Reference: VALUES('', '', '', NULL, NULL, '', '', '', NULL, '', NULL, current_timestamp());
                query = {}
                query['email_queue'] = {}
                query['email_queue']['id'] = str(uuid.uuid4()).upper()
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','id']
                check_field_result = check_field(input_function=copy.deepcopy(query),field=field,type='uuid',default=str(uuid.uuid4()).upper(),optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','email_template_id_fk']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='uuid',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','engine']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(50)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','to']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(500)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','cc']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(500)',default=None,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','bcc']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(500)',default=None,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','subject']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(255)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','message']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777215)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','alt_message']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777215)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # enum
                field = ['email_queue','status']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(50)',default='pending',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # enum
                field = ['email_queue','priority']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=0,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','date']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='datetime',default=None,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','headers']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(65535)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','attachments']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777215)',default='{}',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                query['email_queue']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                #field = ['email_queue','added_on']
                #check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='timestamp',default=str(datetime.datetime.now()).split('.', maxsplit=1)[0],optional=False)
                #if check_field_result['status']:
                #    query = check_field_result['content']
                #else:
                #    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4))
                    execute_query_response = execute_query_email_queues_post(query=query['email_queue'], credentials=credentials)
                    if execute_query_response['status']:
                        if query['email_queue']['priority'] == 1:
                            execute_query_response2 = execute_query_email_queues_patch(query={'status': 'sending'}, credentials=credentials, allwhere="WHERE "+' or '.join(['id=\''+query['email_queue']['id']+'\'']))
                            if execute_query_response2['status']:
                                email_queue = query
                                temp_email_queue = copy.deepcopy(email_queue['email_queue'])
                                if not temp_email_queue['cc']:
                                    temp_email_queue['cc'] = ''
                                if not temp_email_queue['bcc']:
                                    temp_email_queue['bcc'] = ''
                                if not temp_email_queue['attachments'] or temp_email_queue['attachments'] == '':
                                    temp_email_queue['attachments'] = '{}'
                                if temp_email_queue['engine'] == 'gmail':
                                    email_response = send_email(credentials=gmail_credentials,
                                        to=temp_email_queue['to'].split(';'),
                                        cc=temp_email_queue['cc'].split(';'),
                                        bcc=temp_email_queue['bcc'].split(';'),
                                        subject=temp_email_queue['subject'],
                                        message=temp_email_queue['message'],
                                        alt_message=temp_email_queue['alt_message'],
                                        attachments=json.loads(temp_email_queue['attachments']))
                                    if email_response['status']:
                                        set_email_queue = {}
                                        set_email_queue['id'] = temp_email_queue['id']
                                        set_email_queue['status'] = 'sent'
                                        limbo = execute_query_email_queues_patch(query=set_email_queue, credentials=credentials)
                                        #if limbo['status']:
                                        #    print('implementar')
                                        #else:
                                        #    print('implementar')
                                    else:
                                        set_email_queue = {}
                                        set_email_queue['id'] = temp_email_queue['id']
                                        set_email_queue['status'] = 'failed'
                                        limbo = execute_query_email_queues_patch(query=set_email_queue, credentials=credentials)
                                        #if limbo['status']:
                                        #    print('implementar')
                                        #else:
                                        #    print('implementar')
                                        insert_file_log(function='endpoint_email_queues_patch', \
                                            input_function=['email_response False'])
                                else:
                                    insert_file_log(function='send_mail', \
                                        input_function=['engine False'])
                            else:
                                insert_file_log(function='endpoint_email_queues_post', \
                                input_function=['execute_query_response: ',execute_query_response2['content']])
                        #
                        #data = {'message': 'Registro inserido ('+query['email_queue']['id']+')'}
                        data = {'email_queue': {'id': query['email_queue']['id']}}
                        log = {}
                        log['activity_log'] = {}
                        log['activity_log']['id'] = str(uuid.uuid4()).upper()
                        if 'User-Id' in headers:
                            log['activity_log']['user_id_fk'] = headers['User-Id'] #*
                        if 'Channel_Contact_Id' in headers:
                            log['activity_log']['channel_contact_id_fk'] = headers['Channel-Contact-Id'] #*
                        log['activity_log']['rel_id'] = query['email_queue']['id']
                        log['activity_log']['section'] = headers['Section']
                        log['activity_log']['description'] = headers['Description']
                        log['activity_log']['description_complement'] = headers['Description-Complement']
                        log['activity_log']['complementary_information'] = headers['Complementary-Information']
                        log['activity_log']['model'] = ''
                        log['activity_log']['function'] = 'endpoint_email_queues_post'
                        log['activity_log']['result'] = 'Success' #* response 200
                        log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                        log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                        log['activity_log']['ip'] = request.remote_addr #*
                        log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                        insert_activity_log(input_function=log)
                        return jsonify(data), 200
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_email_queues_post', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_email_queues_post', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_email_queues_post', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_email_queues_post', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_email_queues_post: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_email_queues_patch():
    """ doctest for endpoint_email_queues_patch (pendent try exception global of function) without unit test
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
                # SQL Reference: VALUES('', '', '', NULL, NULL, '', '', '', NULL, '', NULL, current_timestamp());
                query = {}
                query['email_queue'] = {}
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','id']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='uuid',default=2,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','email_template_id_fk']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='uuid',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','engine']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(50)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','to']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(500)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','cc']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(500)',default=None,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','bcc']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(500)',default=None,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','subject']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(255)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','message']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777215)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','alt_message']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777215)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # enum
                field = ['email_queue','status']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(50)',default='pending',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','priority']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=0,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','date']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='datetime',default=None,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','headers']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(65535)',default=1,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_queue','attachments']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777215)',default='{}',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4))
                    execute_query_response = execute_query_email_queues_patch(query=query['email_queue'], credentials=credentials)
                    if execute_query_response['status']:
                        #data = {'message': 'Registro atualizado ('+query['email_queue']['id']+')'}
                        data = {'email_queue': {'id': query['email_queue']['id']}}
                        log = {}
                        log['activity_log'] = {}
                        log['activity_log']['id'] = str(uuid.uuid4()).upper()
                        if 'User-Id' in headers:
                            log['activity_log']['user_id_fk'] = headers['User-Id'] #*
                        if 'Channel_Contact_Id' in headers:
                            log['activity_log']['channel_contact_id_fk'] = headers['Channel-Contact-Id'] #*
                        log['activity_log']['rel_id'] = query['email_queue']['id']
                        log['activity_log']['section'] = headers['Section']
                        log['activity_log']['description'] = headers['Description']
                        log['activity_log']['description_complement'] = headers['Description-Complement']
                        log['activity_log']['complementary_information'] = headers['Complementary-Information']
                        log['activity_log']['model'] = ''
                        log['activity_log']['function'] = 'endpoint_email_queues_patch'
                        log['activity_log']['result'] = 'Success' #* response
                        log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                        log['activity_log']['ip'] = request.remote_addr #*
                        log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                        insert_activity_log(input_function=log)
                        return jsonify(data), 200
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_email_queues_patch', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_email_queues_patch', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_email_queues_patch', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_email_queues_patch', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_email_queues_patch: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_email_templates_get():
    """ doctest for endpoint_email_templates_get (pendent try exception global of function) without unit test
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
                    execute_query_response = execute_query_email_templates_get(query=query, credentials=credentials)
                    if execute_query_response['status']:
                        if execute_query_response['content'] or not request.args.get('id'):
                            if (len(execute_query_response['content']) == 1 and request.args.get('id')) or \
                                (len(execute_query_response['content']) >= 0 and not request.args.get('id')):
                                data = execute_query_response['content']
                                log = {}
                                log['activity_log'] = {}
                                log['activity_log']['id'] = str(uuid.uuid4()).upper()
                                if 'User-Id' in headers:
                                    log['activity_log']['user_id_fk'] = headers['User-Id'] #*
                                if 'Channel_Contact_Id' in headers:
                                    log['activity_log']['channel_contact_id_fk'] = headers['Channel-Contact-Id'] #*
                                log['activity_log']['rel_id'] = None #*
                                if (len(execute_query_response['content']) == 1 and request.args.get('id')):
                                    log['activity_log']['rel_id'] = execute_query_response['content'][0]['email_template']['id']
                                log['activity_log']['section'] = headers['Section']
                                log['activity_log']['description'] = headers['Description']
                                log['activity_log']['description_complement'] = headers['Description-Complement']
                                log['activity_log']['complementary_information'] = headers['Complementary-Information']
                                log['activity_log']['model'] = ''
                                log['activity_log']['function'] = 'endpoint_email_templates_get'
                                log['activity_log']['result'] = 'Success' #* response
                                log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                                log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                                log['activity_log']['ip'] = request.remote_addr #*
                                log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                                insert_activity_log(input_function=log)
                                return jsonify(data), 200
                            else:
                                data = {'message': '500 Internal Server Error - Not found uniq'}
                                insert_file_log(function='endpoint_email_templates_get', \
                                    input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - Not found'}
                            insert_file_log(function='endpoint_email_templates_get', \
                                input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_email_templates_get', \
                            input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_email_templates_get', \
                        input_function=['query: ',query,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+str(input_validation_errors)+")"}), 500
            else:
                insert_file_log(function='endpoint_email_templates_get', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_email_templates_get', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_email_templates_get: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_email_templates_post():
    """ doctest for endpoint_email_templates_post (pendent try exception global of function) without unit test
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
                # SQL Reference: VALUES('', '', '', '', '', '', '', 1, current_timestamp());
                query = {}
                query['email_template'] = {}
                query['email_template']['id'] = str(uuid.uuid4()).upper()
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','id']
                check_field_result = check_field(input_function=copy.deepcopy(query),field=field,type='uuid',default=str(uuid.uuid4()).upper(),optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','slug']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(100)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','name']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777515)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','subject']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777515)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','message']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(65535)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','fromname']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777515)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','fromemail']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(100)',default='',optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','active']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=1,optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                query['email_template']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                #field = ['email_template','added_on']
                #check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='timestamp',default=str(datetime.datetime.now()).split('.', maxsplit=1)[0],optional=False)
                #if check_field_result['status']:
                #    query = check_field_result['content']
                #else:
                #    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4))
                    execute_query_response = execute_query_email_templates_post(query=query['email_template'], credentials=credentials)
                    if execute_query_response['status']:
                        #data = {'message': 'Registro inserido ('+query['email_template']['id']+')'}
                        data = {'email_template': {'id': query['email_template']['id']}}
                        log = {}
                        log['activity_log'] = {}
                        log['activity_log']['id'] = str(uuid.uuid4()).upper()
                        if 'User-Id' in headers:
                            log['activity_log']['user_id_fk'] = headers['User-Id'] #*
                        if 'Channel_Contact_Id' in headers:
                            log['activity_log']['channel_contact_id_fk'] = headers['Channel-Contact-Id'] #*
                        log['activity_log']['rel_id'] = query['email_template']['id']
                        log['activity_log']['section'] = headers['Section']
                        log['activity_log']['description'] = headers['Description']
                        log['activity_log']['description_complement'] = headers['Description-Complement']
                        log['activity_log']['complementary_information'] = headers['Complementary-Information']
                        log['activity_log']['model'] = ''
                        log['activity_log']['function'] = 'endpoint_email_templates_post'
                        log['activity_log']['result'] = 'Success' #* response 200
                        log['activity_log']['response'] = json.dumps(data,default=formatter_datetime)
                        log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                        log['activity_log']['ip'] = request.remote_addr #*
                        log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                        insert_activity_log(input_function=log)
                        return jsonify(data), 200
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_email_templates_post', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_email_templates_post', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_email_templates_post', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_email_templates_post', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_email_templates_post: ', exc_type, fname, exc_tb.tb_lineno, str(e))

def endpoint_email_templates_patch():
    """ doctest for endpoint_email_templates_patch (pendent try exception global of function) without unit test
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
                # SQL Reference: VALUES('', '', '', '', '', '', '', 1, current_timestamp());
                query = {}
                query['email_template'] = {}
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','id']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='uuid',default=2,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                else:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','slug']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(100)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','name']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777515)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','subject']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777515)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','message']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(65535)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','fromname']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(16777515)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','fromemail']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='varchar(100)',default='',optional=True)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                field = ['email_template','active']
                check_field_result = check_field(input_function=copy.deepcopy(request_json),field=field,type='tinyint(4)',default=1,optional=False)
                if check_field_result['status']:
                    pathset(query, field, pathget(check_field_result['content'], field)['content'])
                elif not '_field(s);' in check_field_result['content']:
                    input_validation_errors += check_field_result['content']
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                if not input_validation_errors:
                    #print('pos request_json',json.dumps(query,indent=4))
                    execute_query_response = execute_query_email_templates_patch(query=query['email_template'], credentials=credentials)
                    if execute_query_response['status']:
                        #data = {'message': 'Registro atualizado ('+query['email_template']['id']+')'}
                        data = {'email_template': {'id': query['email_template']['id']}}
                        log = {}
                        log['activity_log'] = {}
                        log['activity_log']['id'] = str(uuid.uuid4()).upper()
                        if 'User-Id' in headers:
                            log['activity_log']['user_id_fk'] = headers['User-Id'] #*
                        if 'Channel_Contact_Id' in headers:
                            log['activity_log']['channel_contact_id_fk'] = headers['Channel-Contact-Id'] #*
                        log['activity_log']['rel_id'] = query['email_template']['id']
                        log['activity_log']['section'] = headers['Section']
                        log['activity_log']['description'] = headers['Description']
                        log['activity_log']['description_complement'] = headers['Description-Complement']
                        log['activity_log']['complementary_information'] = headers['Complementary-Information']
                        log['activity_log']['model'] = ''
                        log['activity_log']['function'] = 'endpoint_email_templates_patch'
                        log['activity_log']['result'] = 'Success' #* response
                        log['activity_log']['json'] = json.dumps(query,default=formatter_datetime) #* request
                        log['activity_log']['ip'] = request.remote_addr #*
                        log['activity_log']['added_on'] = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
                        insert_activity_log(input_function=log)
                        return jsonify(data), 200
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function='endpoint_email_templates_patch', \
                            input_function=['request_json: ',request_json,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function='endpoint_email_templates_patch', \
                        input_function=['request_json: ',request_json,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+input_validation_errors+")"}), 500
            else:
                insert_file_log(function='endpoint_email_templates_patch', \
                    input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function='endpoint_email_templates_patch', \
                input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_email_templates_patch: ', exc_type, fname, exc_tb.tb_lineno, str(e))
