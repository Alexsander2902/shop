""" __init__.py """

# Utils
from app.utils.util import load_json

import mysql.connector

credentials = load_json(file='./constants/database.json')
credentials = credentials['conn_local']

from app.utils.util import timer

def get_connection(credentials={}):
    execute_query_response = {}
    execute_query_response['status'] = False
    execute_query_response['content'] = []
    conn = None
    try:
        conn = mysql.connector.connect(user=credentials['user'],password=credentials['password'],host=credentials['host'],port=credentials['port'],database=credentials['database'])
    except Exception as error:
        execute_query_response['content'] = str(error)
    if conn is not None:
        execute_query_response['status'] = True
        execute_query_response['content'] = conn
    return execute_query_response

def execute_query_connection(cur=None,content='',query={}):
    execute_query_response = {}
    execute_query_response['status'] = False
    execute_query_response['content'] = {}
    try:
        if 'SELECT' in content:
            cur.execute(content, (query))
            fetchall_response = cur.fetchall()
            execute_query_response['status'] = True
            execute_query_response['content'] = fetchall_response
        elif 'INSERT' in content or 'UPDATE' in content:
            cur.execute(content, (query))
            execute_query_response['status'] = True
    except Exception as error:
        sql = ''
        try:
            sql = content % query
        except Exception:
            sql = str(content) + ' : ' + str(query)
            pass
        execute_query_response['content'] = str(error) + ' : ' + str(sql)
    return execute_query_response


def execute_query_get_max_order(table=''):
    """ doctest for execute_query_get_max_order (pendent try exception global of function) without unit test
    """
    global credentials
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
            content = "SELECT `order` FROM "+table+" ORDER BY `order` desc limit 1;"
            query1 = execute_query_connection(cur=cur,content=content)
            if query1['status']:
                temp_response = query1['content']
                if temp_response:
                    for item in temp_response:
                        temp_dict_response = {}
                        temp_dict_response[table] = {}
                        temp_dict_response[table]['order'] = item[0] + 1
                        execute_query_response['content'].append(temp_dict_response)
                    execute_query_response['status'] = True
                else:
                    execute_query_response['content'].append({table: {'order': 1}})
                    execute_query_response['status'] = True
            cur.close()
            conn.close()
        else:
            execute_query_response['content'] = conn['content']
    #except Exception as error:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error execute_query_get_max_order: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response
