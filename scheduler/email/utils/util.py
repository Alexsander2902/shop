""" util.py """

import datetime

def save_file(file='logs/'+str(datetime.datetime.now()).split(' ', maxsplit=1)[0]+'.log',content=''):
    """ save_file
    """
    file = open(file,'a', encoding="utf-8")
    file.write(content+'\n')
    file.close()

def insert_file_log(function='',input_function=[]):
    """ insert_file_log
    """
    save_file(content='  ERROR - '+str(datetime.datetime.now()).split('.', maxsplit=1)[0]+' --> '+function+': '+ str(input_function))
