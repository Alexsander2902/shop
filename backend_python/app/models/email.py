""" email.py """

# Libraries
import mysql.connector

from app.models import get_connection
from app.models import execute_query_connection

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

            if query["response_type"]=='table_data':
                content = "SELECT id, email_template_id_fk, engine, `to`, cc, bcc, subject, message, alt_message, status, priority, date, headers, attachments, added_on FROM email_queue" 
                
            content += where + order + limit
            
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            if query1['status']:
                temp_response = query1['content']
                if temp_response:
                    keys = ('id','email_template_id_fk','engine','to','cc','bcc','subject','message','alt_message','status','priority','date','headers','attachments','added_on',) # email_queue 15 (15)
                    
                    for item in temp_response:
                        temp_dict_response = {}
                        temp_dict_response['email_queue'] = {keys[i]:item[i] for i in range(15)}

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

def execute_query_email_queues_post(query={}, credentials={}):
    """ doctest for execute_query_email_queues_post (pendent try exception global of function) without unit test
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
            content = "INSERT INTO email_queue" \
                "(id, email_template_id_fk, engine, `to`, cc, bcc, subject, message, alt_message, status, priority, `date`, headers, attachments, added_on) " \
                "VALUES(%(id)s, %(email_template_id_fk)s, %(engine)s, %(to)s, %(cc)s, %(bcc)s, %(subject)s, %(message)s, %(alt_message)s, %(status)s, %(priority)s, %(date)s, %(headers)s, %(attachments)s, %(added_on)s)"
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
    #    print('Error execute_query_individuals_post: ', exc_type, fname, exc_tb.tb_lineno, str(error))
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

def execute_query_email_templates_get(query={}, credentials={}):
    """ doctest for execute_email_templates_get (pendent try exception global of function) without unit test
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
            where = ' where excluded=0'
            order = ' order by added_on desc'
            limit = ''

            if query["id"]:
                where += " and id=%(id)s"

            if query["search"]:
                where += " and name like '%' %(search)s '%'"

            if query["order_column_1"]:
                order = " order by " + query['order_column_1'] + " " + query['order_direction_column_1']

            if query["limit"]:
                limit = " limit " + query["limit"]

            if query["response_type"] == 'table_data':
                content = "SELECT id, slug, name, subject, message, fromname, fromemail, active, excluded, added_on FROM email_template" 

            if query["response_type"] == 'custom_data_1':
                content = "SELECT id, slug, name, subject, message, fromname, fromemail, active, excluded, added_on FROM email_template" 

            content += where + order + limit
            query1 = execute_query_connection(cur=cur,content=content,query=query)
            
            if query1['status']:
                temp_response = query1['content']
                if temp_response:
                    keys = ('id','slug','name','subject','message','fromname','fromemail','active','excluded', 'added_on') # email_template 10 (10)
                    keys_custom_data_1 = ('id','slug','name','subject','message','fromname','fromemail','active','excluded', 'added_on') # email_template 10 (10)

                    for item in temp_response:
                        temp_dict_response = {}

                        if query["response_type"] == 'table_data':
                            temp_dict_response['email_template'] = {keys[i]:item[i] for i in range(10)}

                        if query["response_type"] == 'custom_data_1':
                            temp_dict_response['email_template'] = {keys_custom_data_1[i]:item[i] for i in range(10)}
                        
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
    #    print('Error execute_query_email_template_get: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_email_templates_post(query={}, credentials={}):
    """ doctest for execute_query_email_templates_post (pendent try exception global of function) without unit test
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
            content = "INSERT INTO email_template" \
                "(id, slug, name, subject, message, fromname, fromemail, active, added_on) " \
                "VALUES (%(id)s, %(slug)s, %(name)s, %(subject)s, %(message)s, %(fromname)s, %(fromemail)s, %(active)s, %(added_on)s)"
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
    #    print('Error execute_query_individuals_post: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response

def execute_query_email_templates_patch(query={}, credentials={}):
    """ doctest for execute_query_email_templates_patch (pendent try exception global of function) without unit test
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
            if 'slug' in query:
                partial_query += ' slug=%(slug)s,'
            if 'name' in query:
                partial_query += ' name=%(name)s,'
            if 'subject' in query:
                partial_query += ' subject=%(subject)s,'
            if 'message' in query:
                partial_query += ' message=%(message)s,'
            if 'fromname' in query:
                partial_query += ' fromname=%(fromname)s,'
            if 'fromemail' in query:
                partial_query += ' fromemail=%(fromemail)s,'
            if 'active' in query:
                partial_query += ' active=%(active)s,'
            partial_query = partial_query[:-1] + ' '
            content = "UPDATE email_template " \
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
    #    print('Error execute_query_individuals_patch: ', exc_type, fname, exc_tb.tb_lineno, str(error))
    return execute_query_response
