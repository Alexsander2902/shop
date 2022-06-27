""" __init__.py """

import json

import mysql.connector

def load_json(file='file.json'):
    """ load_json
    """
    file = open(file,'r')
    raw = file.read()
    file.close()
    return json.loads(raw)

credentials = load_json(file='./models/database.json')

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