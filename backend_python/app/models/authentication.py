""" user.py """

# Libraries
import mysql.connector

from app.models import get_connection
from app.models import execute_query_connection

def execute_query_authentication_post(query={}, credentials={}):
    """ doctest for execute_query_authentication_post (pendent try exception global of function) without unit test
    """
    execute_query_response = {}
    execute_query_response['status'] = False
    execute_query_response['content'] = []
    #try:
    if True:
        # Connection
        conn = get_connection(credentials=credentials)
        if conn['status']:
            conn = conn['content']
            # Get Cursor
            cur = conn.cursor()
            content = "SELECT `user`.id, `user`.individual_id_fk, `user`.alias, `user`.login, `user`.password, `user`.pagination, `user`.active, `user`.excluded, `user`.added_on " \
                "FROM `user` " \
                "WHERE `user`.login=%(login)s and `user`.excluded=0 and `user`.active=1;"
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                temp_response = query1['content']
                
                for item in temp_response:
                    temp_dict_response = {}
                    temp_dict_response['user'] = {}
                    temp_dict_response['user']['id'] = item[0]
                    temp_dict_response['user']['individual_id_fk'] = item[1]
                    temp_dict_response['user']['alias'] = item[2]
                    temp_dict_response['user']['login'] = item[3]
                    temp_dict_response['user']['password'] = item[4]
                    temp_dict_response['user']['pagination'] = item[5]
                    temp_dict_response['user']['active'] = item[6]
                    temp_dict_response['user']['excluded'] = item[7]
                    temp_dict_response['user']['added_on'] = str(item[8])

                    execute_query_response['content'].append(temp_dict_response)

                execute_query_response['status'] = True
            else:
                execute_query_response['content'] = query1['content']
            cur.close()
            conn.close()
        else:
            execute_query_response['content'] = conn['content']
    #except Exception as error:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error execute_query_authentication_post: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_user_auto_login_get(query={}, credentials={}):
    """ doctest for execute_query_user_auto_login_get (pendent try exception global of function) without unit test
    """
    execute_query_response = {}
    execute_query_response['status'] = False
    execute_query_response['content'] = []
    #try:
    if True:
        # Connection
        conn = get_connection(credentials=credentials)
        if conn['status']:
            conn = conn['content']
            # Get Cursor
            cur = conn.cursor()
            content = "SELECT id, user_id_fk, user_hash, added_on FROM user_auto_login WHERE user_id_fk=%(user_id_fk)s AND user_hash=%(user_hash)s;"
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                temp_response = query1['content']
                keys = ('id','user_id_fk','user_hash','added_on')

                for item in temp_response:
                    temp_dict_response = {}
                    temp_dict_response['user_auto_login'] = {keys[i]:item[i] for i in range(4)}

                    execute_query_response['content'].append(temp_dict_response)
                execute_query_response['status'] = True
            else:
                execute_query_response['content'] = query1['content']
            cur.close()
            conn.close()
        else:
            execute_query_response['content'] = conn['content']
    #except Exception as error:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error execute_query_individuals_get: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_user_auto_login_post(query={}, credentials={}):
    """ doctest for execute_query_user_auto_login_post (pendent try exception global of function) without unit test
    """
    execute_query_response = {}
    execute_query_response['status'] = False
    execute_query_response['content'] = []
    #try:
    if True:
        # Connection
        conn = get_connection(credentials=credentials)
        if conn['status']:
            conn = conn['content']
            # Get Cursor
            cur = conn.cursor()
            content = "INSERT INTO user_auto_login" \
                "(id, user_id_fk, user_hash, added_on) VALUES(%(id)s, %(user_id_fk)s, %(user_hash)s, %(added_on)s)"
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                conn.commit()
                execute_query_response['status'] = True
            else:
                execute_query_response['content'] = query1['content']
            cur.close()
            conn.close()
        else:
            execute_query_response['content'] = conn['content']
    #except Exception as error:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error execute_query_individuals_get: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

