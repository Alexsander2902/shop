""" misc.py """

# Libraries
import mysql.connector
from app.models import get_connection
from app.models import execute_query_connection

import uuid

def execute_query_activity_log_post(query={}, credentials={}):
    """ doctest for execute_query_activity_log_post (pendent try exception global of function) without unit test
    """
    execute_query_response = {}
    execute_query_response['status'] = False
    execute_query_response['content'] = None
    #try:
    if True:
        # Connection
        conn = get_connection(credentials=credentials)
        if conn['status']:
            conn = conn['content']
            # Get Cursor
            cur = conn.cursor()
            content = "INSERT INTO activity_log" \
                "(id, user_id_fk, rel_id, `section`, model, `function`, `result`, description, description_complement, complementary_information, response, json, ip, added_on) " \
                "VALUES(%(id)s, %(user_id_fk)s, %(rel_id)s, %(section)s, %(model)s," \
                " %(function)s, %(result)s, %(description)s, %(description_complement)s," \
                " %(complementary_information)s, %(response)s, %(json)s, %(ip)s, %(added_on)s)"
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
    #    print('Error execute_query_activity_log_post: ', exc_type, fname, exc_tb.tb_lineno, str(error))

    return execute_query_response

def execute_query_activity_logs_get(query={}, credentials={}):
    """ doctest for execute_query_activity_logs_get (pendent try exception global of function) without unit test
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
            where = ''
            order = ' order by activity_log.added_on desc'
            limit = ''

            if query["id"]:
                where += " and activity_log.id=%(id)s"

            if query["order_column_1"]:
                order = " order by " + query['order_column_1'] + " " + query['order_direction_column_1']

            if query["limit"]:
                limit = " limit " + query["limit"]

            if query["response_type"] == 'table_data':
                content = "SELECT activity_log.id, activity_log.user_id_fk, activity_log.rel_id, activity_log.section, activity_log.model, activity_log.function, activity_log.result, activity_log.description, activity_log.description_complement, activity_log.complementary_information, activity_log.response, activity_log.json, activity_log.ip, activity_log.added_on FROM activity_log"
                
            content += where + order + limit
            
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                temp_response = query1['content']
                if temp_response:
                    for item in temp_response:
                        temp_dict_response = {}
                        temp_dict_response['activity_log'] = {}
                        temp_dict_response['activity_log']['user_id_fk'] = item[0]
                        temp_dict_response['activity_log']['rel_id'] = item[1]
                        temp_dict_response['activity_log']['section'] = item[2]
                        temp_dict_response['activity_log']['model'] = item[3]
                        temp_dict_response['activity_log']['function'] = item[4]
                        temp_dict_response['activity_log']['result'] = item[5]
                        temp_dict_response['activity_log']['description'] = item[6]
                        temp_dict_response['activity_log']['description_complementary'] = item[7]
                        temp_dict_response['activity_log']['description_information'] = item[8]
                        temp_dict_response['activity_log']['response'] = item[9]
                        temp_dict_response['activity_log']['json'] = item[10]
                        temp_dict_response['activity_log']['ip'] = item[11]
                        temp_dict_response['activity_log']['added_on'] = str(item[12])
                        
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
    #    print('Error execute_query_activity_logs_get: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response
