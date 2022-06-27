""" email.py """

# Libraries
import mysql.connector

from models import get_connection
from models import execute_query_connection

def execute_query_email_queues_get(query={}, credentials={}):
    """ doctest for execute_query_email_queues_get (pendent try exception global of function) without unit test
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
            where = ' where 1=1'
            order = ' order by added_on desc'
            limit = ''

            if query["id"]:
                where += ' and id=%(id)s' 

            if query["order_column_1"]:
                order = " order by " + query['order_column_1'] + " " + query['order_direction_column_1']

            if query["limit"]:
                limit = " limit " + query["limit"]

            content = "SELECT id, engine, `to`, cc, bcc, subject, message, alt_message, status, priority, date, headers, attachments, added_on FROM email_queue" + where + order + limit
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                temp_response = query1['content']
                if temp_response:
                    for item in temp_response:
                        temp_dict_response = {}
                        temp_dict_response['email_queue'] = {}
                        temp_dict_response['email_queue']['id'] = item[0]
                        temp_dict_response['email_queue']['email_template_id_fk'] = item[1]
                        temp_dict_response['email_queue']['engine'] = item[2]
                        temp_dict_response['email_queue']['to'] = item[3]
                        temp_dict_response['email_queue']['cc'] = item[4]
                        temp_dict_response['email_queue']['bcc'] = item[5]
                        temp_dict_response['email_queue']['subject'] = item[6]
                        temp_dict_response['email_queue']['message'] = item[7]
                        temp_dict_response['email_queue']['alt_message'] = item[8]
                        temp_dict_response['email_queue']['status'] = item[9]
                        temp_dict_response['email_queue']['priority'] = item[10]
                        temp_dict_response['email_queue']['date'] = item[11]
                        temp_dict_response['email_queue']['headers'] = item[12]
                        temp_dict_response['email_queue']['attachments'] = item[13]
                        temp_dict_response['email_queue']['added_on'] = str(item[14])
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
    #    print('Error execute_query_email_queues_get: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_email_queues_patch(query={}, credentials={}, allwhere="WHERE id=%(id)s"):
    """ doctest for execute_query_email_queues_patch (pendent try exception global of function) without unit test
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
            if 'email_template_id_fk' in query:
                partial_query += ' email_template_id_fk=%(email_template_id_fk)s,'
            if 'engine' in query:
                partial_query += ' engine=%(engine)s,'
            if 'to' in query:
                partial_query += ' `to`=%(to)s,'
            if 'cc' in query:
                partial_query += ' cc=%(cc)s,'
            if 'subject' in query:
                partial_query += ' subject=%(subject)s,'
            if 'bcc' in query:
                partial_query += ' bcc=%(bcc)s,'
            if 'message' in query:
                partial_query += ' message=%(message)s,'
            if 'alt_message' in query:
                partial_query += ' alt_message=%(alt_message)s,'
            if 'status' in query:
                partial_query += ' status=%(status)s,'
            if 'priority' in query:
                partial_query += ' priority=%(priority)s,'
            if 'date' in query:
                partial_query += ' `date`=%(date)s,'
            if 'headers' in query:
                partial_query += ' headers=%(headers)s,'
            if 'attachments' in query:
                partial_query += ' attachments=%(attachments)s,'
            if 'active' in query:
                partial_query += ' active=%(active)s,'
            if 'excluded' in query:
                partial_query += ' excluded=%(excluded)s,'
            partial_query = partial_query[:-1] + ' '
            content = "UPDATE email_queue " \
                +partial_query+ \
                allwhere
            #print(query)
            #print(content)
            #print(content%query)
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
    #    print('Error execute_query_individuals_patch: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response
