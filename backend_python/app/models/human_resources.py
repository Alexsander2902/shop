""" human_resources.py """

# Libraries
import mysql.connector

from app.models import get_connection
from app.models import execute_query_connection

def execute_query_genders_get(query={}, credentials={}):
    """ doctest for execute_query_genders_get (pendent try exception global of function) without unit test
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
            where = ' where gender.excluded=0'
            order = ' order by gender.added_on desc'
            limit = ''

            if query["id"]:
                where += " and gender.id=%(id)s"

            if query["search"]:
                where += " and gender.name like '%' %(search)s '%'"

            if query["order_column_1"]:
                order = " order by " + query['order_column_1'] + " " + query['order_direction_column_1']

            if query["limit"]:
                limit = " limit " + query["limit"]

            if query["response_type"] == 'table_data':
                content = "SELECT id, name, `order`, active, excluded, added_on FROM gender"
            
            if query["response_type"] == 'custom_data_1':
                content = "SELECT gender.id, gender.name, gender.`order`, gender.active, gender.added_on " \
                    "FROM gender " \
                    "LEFT JOIN individual ON individual.gender_id_fk = gender.id " \
                    "LEFT JOIN staff ON staff.individual_id_fk = individual.id"

            content += where + order + limit
            
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                temp_response = query1['content']
                if temp_response:

                    for item in temp_response:
                        temp_dict_response = {}

                        if query["response_type"] == 'table_data':
                            temp_dict_response['gender'] = {}
                            temp_dict_response['gender']['id'] = item[0]
                            temp_dict_response['gender']['name'] = item[1]
                            temp_dict_response['gender']['order'] = item[2]
                            temp_dict_response['gender']['active'] = item[3]
                            temp_dict_response['gender']['excluded'] = item[4]
                            temp_dict_response['gender']['added_on'] = item[5]

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
    #    print('Error execute_query_genders_get: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_genders_post(query={}, credentials={}):
    """ doctest for execute_query_genders_post (pendent try exception global of function) without unit test
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
            content = "INSERT INTO gender" \
                "(id, name, `order`, active, added_on) " \
                "VALUES (%(id)s, %(name)s, %(order)s, %(active)s, %(added_on)s)"
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
    #    print('Error execute_query_genders_post: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_genders_patch(query={}, credentials={}):
    """ doctest for execute_query_genders_patch (pendent try exception global of function) without unit test
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
            partial_query = 'SET'
            if 'name' in query:
                partial_query += ' name=%(name)s,'
            if 'order' in query:
                partial_query += ' `order`=%(order)s,'
            if 'active' in query:
                partial_query += ' active=%(active)s,'
            if 'excluded' in query:
                partial_query += ' excluded=%(excluded)s,'
            partial_query = partial_query[:-1] + ' '
            content = "UPDATE gender " \
                +partial_query+ \
                "WHERE id=%(id)s"
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
    #    print('Error execute_query_genders_patch: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_users_get(query={}, credentials={}):
    """ doctest for execute_query_users_get (pendent try exception global of function) without unit test
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
            where = ' where user.excluded=0'
            order = ' order by user.added_on desc'
            limit = ''

            if query["id"]:
                where += " and user.id= %(id)s"

            if query["search"]:
                where += " and individual.name like '%' %(search)s '%'"

            if query["limit"]:
                limit = " limit " + query["limit"]

            if query["response_type"] == 'table_data':
                content ="SELECT user.id, user.individual_id_fk, user.alias, user.login, user.password, user.pagination, user.active, user.admin, user.excluded, user.added_on FROM user "

            if query["response_type"] == 'custom_data_1' or query["response_type"] == 'custom_data_2' or query["response_type"] == 'custom_data_3' or query["response_type"] == 'custom_data_4' or query["response_type"] == 'custom_data_5' or query["response_type"] == 'custom_data_6' or query["response_type"] == 'custom_data_7' or query["response_type"] == 'custom_data_8' or query["response_type"] == 'custom_data_9' or query["response_type"] == 'custom_data_10':
                content ="SELECT user.id, user.individual_id_fk, user.alias, user.login, user.password, user.pagination, user.active, user.admin, user.excluded, user.added_on, user.id, user.alias, user.login, user.active, user.added_on, individual.id, individual.name " \
                    "FROM user " \
                    "INNER JOIN individual " \
                    "ON individual.id = user.individual_id_fk "

            if not query["response_type"]:
                content = "SELECT user.id, user.individual_id_fk, user.alias, user.login, user.password, user.pagination, user.active, user.admin, user.excluded, user.added_on FROM user " 

            content += where + order + limit    

            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                temp_response = query1['content']
                if temp_response:

                    for item in temp_response:
                        temp_dict_response = {}

                        if query["response_type"] == 'table_data': 
                            temp_dict_response['user'] = {}
                            temp_dict_response['user']['id'] = item[0]
                            temp_dict_response['user']['individual_id_fk'] = item[1]
                            temp_dict_response['user']['alias'] = item[2]
                            temp_dict_response['user']['login'] = item[3]
                            temp_dict_response['user']['password'] = item[4]
                            temp_dict_response['user']['pagination'] = item[5]
                            temp_dict_response['user']['active'] = item[6]
                            temp_dict_response['user']['admin'] = item[7]
                            temp_dict_response['user']['excluded'] = item[8]
                            temp_dict_response['user']['added_on'] = item[9]

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
    #    print('Error execute_query_users_get: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_users_post(query={}, credentials={}):
    """ doctest for execute_query_users_post (pendent try exception global of function) without unit test
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
            
            content = "INSERT INTO `user`" \
                "(id, individual_id_fk, alias, login, password, pagination, active, admin, added_on) " \
                "VALUES (%(id)s, %(individual_id_fk)s, %(alias)s, %(login)s, %(password)s, %(pagination)s, %(active)s, %(admin)s, %(added_on)s)"
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
    #    print('Error execute_query_users_post: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_users_patch(query={}, credentials={}):
    """ doctest for execute_query_users_patch (pendent try exception global of function) without unit test
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
            partial_query = 'SET'
            if 'individual_id_fk' in query:
                partial_query += ' individual_id_fk=%(individual_id_fk)s,'
            if 'alias' in query:
                partial_query += ' alias=%(alias)s,'
            if 'login' in query:
                partial_query += ' login=%(login)s,'
            if 'password' in query:
                partial_query += ' password=%(password)s,'
            if 'pagination' in query:
                partial_query += ' pagination=%(pagination)s,'
            if 'active' in query:
                partial_query += ' active=%(active)s,'
            if 'admin' in query:
                partial_query += ' admin=%(admin)s,'              
            if 'excluded' in query:
                partial_query += ' excluded=%(excluded)s,'
            partial_query = partial_query[:-1] + ' '
            content = "UPDATE `user` " \
                +partial_query+ \
                "WHERE id=%(id)s"
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
    #    print('Error execute_query_users_patch: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response
