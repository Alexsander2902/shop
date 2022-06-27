""" main.py """

import schedule
import time

##roda em "fila" se ambas as funções sao usadas ao mesmo tempo (atrasa a nova que foi chamada)
#import datetime
#s = -1
#def run():
#    global s
#    s = s + 1
#    for x in range (0,70):
#        print(str(datetime.datetime.now()),'Runned!',s)
#        time.sleep(1)

from models import credentials as database_credentials
from models.email import execute_query_email_queues_get
from models.email import execute_query_email_queues_patch
from utils.gmail import send_email

from utils.util import insert_file_log
import json
import copy

def load_file(file='./utils/email.html'):
    file = open(file,'r')
    raw = file.read()
    file.close()
    return raw

gmail_credentials = json.loads(load_file(file='./gmail.json'))

def send_mail():
    list_ids = []
    email_queues_list = execute_query_email_queues_get(credentials=database_credentials, allwhere=' WHERE status = \'pending\' ORDER BY added_on desc') # and date < datetime.now()?
    if email_queues_list['status']:
        for email_queue in email_queues_list['content']:
            list_ids.append('id=\''+email_queue['email_queue']['id']+'\'')
        if list_ids:
            execute_query_response = execute_query_email_queues_patch(query={'status': 'sending'}, credentials=database_credentials, allwhere="WHERE "+' or '.join(list_ids))
            if execute_query_response['status']:
                print('execute_query_email_queues_patch OK')
                for email_queue in email_queues_list['content']:
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
                            execute_query_email_queues_patch(query=set_email_queue, credentials=database_credentials)
                        else:
                            set_email_queue = {}
                            set_email_queue['id'] = temp_email_queue['id']
                            set_email_queue['status'] = 'failed'
                            execute_query_email_queues_patch(query=set_email_queue, credentials=database_credentials)
                            insert_file_log(function='endpoint_email_queues_patch', \
                                input_function=['email_response False'])
                    else:
                        insert_file_log(function='send_mail', \
                            input_function=['engine False'])
            else:
                insert_file_log(function='send_mail', \
                    input_function=['execute_query_email_queues_patch False'])
        else:
            insert_file_log(function='send_mail', \
                input_function=['list_ids False'])
    else:
        insert_file_log(function='send_mail', \
            input_function=['email_queues_list False'])

schedule.every(1).minutes.do(send_mail)

if __name__ == '__main__':
    send_mail()
    while 1:
      schedule.run_pending()
      time.sleep(1)

#teste
#from utils.gmail import send_email
#email_response = send_email(subject='Subject',
#    to=['testedeenvio@credihabitar.com.br'],
#    cc=['testedeenvio@credihabitar.com.br'],
#    bcc=['testedeenvio@credihabitar.com.br']
#    )