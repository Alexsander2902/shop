""" util.py """

# Libraries
import re
import datetime
import json
import bcrypt

import functools
import time
import pandas as pd

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        text='[' + func.__name__ + '] ' + "Elapsed time: {:0.4f} seconds"
        print(text.format(elapsed_time))
        return value
    return wrapper_timer

def save_file(file='logs/'+str(datetime.datetime.now()).split(' ', maxsplit=1)[0]+'.log',content=''):
    """ save_file
    """
    file = open(file,'a', encoding="utf-8")
    file.write(content+'\n')
    file.close()

def load_file(file='./utils/email.html'):
    file = open(file,'r')
    raw = file.read()
    file.close()
    return raw

def load_excell_file(file='logs/'+str(datetime.datetime.now()).split(' ', maxsplit=1)[0]+'.log',content=''):
    df1 = pd.read_excel(file,sheet_name=None)
    sheet_content = {}
    for key in df1:
        sheet_content[key] = df1[key].to_json()
    return sheet_content

def generate_password(passwd):
    """ generate_password
    """
    passwd = passwd.encode('ascii')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed

def check_password(passwd, hashed):
    """ check_password
    """
    passwd = passwd.encode('ascii')
    hashed = hashed.encode('ascii')
    if bcrypt.checkpw(passwd, hashed):
        return True
    else:
        return False

def check_uuid(txt):
    """
    >>> check_uuid('')
    True
    >>> check_uuid('')
    False
    """
    try:
        if txt:
            if re.search("^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$", txt):
                return True
            else:
                return False
        else:
            # No txt to check
            return True
    except Exception as error:
        print('Error check_uuid: ',str(error))
        return False

def check_input(input_function="None",field='field',type='type',default='default',optional=True):
    """ check_input
    """
    check_input_response = {}
    check_input_response['status'] = False
    check_input_response['content'] = ""
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if type == "timestamp" or type == "datetime":
        if input_function is not None:
            if isinstance(input_function, str): #Correct -> True
                try: #Correct -> True
                    datetime.datetime.strptime(input_function, "%Y-%m-%d %H:%M:%S")
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                except Exception as error: #Incorrect -> False
                    print("Error check_input timestamp: "+str(error))
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "date":
        if input_function is not None:
            if isinstance(input_function, str): #Correct -> True
                try: #Correct -> True
                    datetime.datetime.strptime(input_function, "%Y-%m-%d")
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                except Exception as error: #Incorrect -> False
                    print("Error check_input date: "+str(error))
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif "decimal" in type:
        if input_function is not None:
            if isinstance(input_function, float): #Correct -> True
                if "e" in str(input_function):
                    input_function = f"{input_function:f}"
                if int(type.split('(')[1].split(')')[0].split(',')[0]) >= len(str(input_function).split('.')[0]) and int(type.split('(')[1].split(')')[0].split(',')[1]) >= len(str(input_function).split('.')[1]): #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif "char" in type: #varchar 14 25 45 50 60 75 100, mediumtext == varchar(16,777,215) (2^2 7 - 1) bytes = 16 MiB, text == varchar(65,535)
        if input_function is not None:
            if isinstance(input_function, str): #Correct -> True
                if int(type.split('(')[1].split(')')[0]) >= len(input_function): #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "int(11)": #2^32
        if input_function is not None:
            if isinstance(input_function, int): #Correct -> True
                if input_function >= -2147483648 and 2147483647 >= input_function: #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "login":
        if input_function is not None:
            if isinstance(input_function, str): #Correct -> True
                if len(input_function) >= 1 and 75 >= len(input_function): #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "password":
        if input_function is not None:
            if isinstance(input_function, str): #Correct -> True
                if len(input_function) >= 1 and 60 >= len(input_function): #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "uuid":
        if input_function is not None:
            if isinstance(input_function, str): #Correct -> True
                if check_uuid(input_function): #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "smalint(6)": #8^6
        if input_function is not None:
            if isinstance(input_function, int): #Correct -> True
                if input_function >= -32768 and 32767 >= input_function: #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "tinyint(4)": #4^4
        if input_function is not None:
            if isinstance(input_function, int): #Correct -> True
                if input_function >= -128 and 127 >= input_function: #Correct -> True
                    check_input_response['content'] = input_function
                    check_input_response['status'] = True
                else: #Incorrect -> False
                    check_input_response['content'] += field+'_content;'
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    elif type == "boolean":
        if input_function is not None:
            if isinstance(input_function, bool): #Correct -> True
                check_input_response['content'] = input_function
                check_input_response['status'] = True
            else: #Incorrect -> False
                check_input_response['content'] += field+'_content_type;'
        else:
            if optional: #Null opt. -> Default
                check_input_response['content'] = default
                check_input_response['status'] = True
            else: #Null obr.(notnull) -> Error
                check_input_response['content'] += field+'_empty_content;'
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    else:
        print("Type not found")
    return check_input_response

def pathget_and_create(dictionary, path):
    """ pathget_and_create
    """
    for item in path:
        if item not in dictionary:
            dictionary[item] = {}
        elif not isinstance(dictionary[item], dict):
            dictionary[item] = {}
        dictionary = dictionary[item]
    return dictionary

def pathget(dictionary, path):
    """ pathget
    """
    function_response = {}
    function_response['status'] = False
    function_response['content'] = ""
    try:
        for item in path:
            dictionary = dictionary[item]
        function_response['status'] = True
        function_response['content'] = dictionary
    except Exception as error:
        print('Error pathget: '+str(error))
    return function_response

def pathset(dictionary, path, setItem):
    """ pathset
    """
    key = path[-1]
    dictionary = pathget_and_create(dictionary, path[:-1])
    #if not isinstance(dictionary, dict):
    #    dictionary = {}
    dictionary[key] = setItem

def check_field(input_function="None",field=['field'],type='type',default='default',optional=False):
    """ check_field
    """
    check_field_response = {}
    check_field_response['status'] = False
    check_field_response['content'] = ""
    # change params output from reference to value
    path = pathget(input_function,field)
    output = {}
    if path['status']: #pendent function sub fields validation
        check_field_result = check_input(input_function=path['content'],field=str(field),type=type,optional=optional,default=default)
        #print(check_field_result)
        if check_field_result['status']:
            pathset(output, field, check_field_result['content'])
            check_field_response['status'] = True
            check_field_response['content'] = output
        else:
            check_field_response['content'] += check_field_result['content']

    else:
        if optional: #Without obr.(notnull) -> Default
            pathset(output, field, default) #to create path?
            pathset(output, field, default) #to set value?
            check_field_response['status'] = True
            check_field_response['content'] = output
        else: #Without opt. -> Error
            check_field_response['content'] += str(field)+'_field(s);'
    return check_field_response

@timer
def check_header(header={},key=''):
    """ doctest for check_key (pendent try exception global of function) without unit test
    """
    function_response = {}
    function_response['status'] = False
    function_response['content'] = None
    if 'Key' in header and 'Section' in header and 'Description' in header and 'Description-Complement' in header and 'Complementary-Information' in header:
        if isinstance(header['Key'], str):
            if len(header['Key']) == 32:
                if header['Key'] == key:
                    function_response['status'] = True
                else:
                    function_response['content'] = 'Incorret Key value'
            else:
                function_response['content'] = 'Incorret Key lenght'
        else:
            function_response['content'] = 'Incorret Key type'
    else:
        function_response['content'] = 'Not found Key, Section, Description, Description-Complement or Complementary-Information'
    return function_response

def insert_file_log(function='',input_function=[]):
    """ insert_file_log
    """
    save_file(content='  ERROR - '+str(datetime.datetime.now()).split('.', maxsplit=1)[0]+' --> '+function+': '+ str(input_function))

def formatter_datetime(o):
    """ formatter_datetime
    """
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def load_json(file='file.json'):
    """ load_json
    """
    file = open(file,'r')
    raw = file.read()
    file.close()
    return json.loads(raw)

def diff_days(value1:str, value2:str) -> int:
    """ Time difference in days
    """
    value1 = value1[0:10]
    value2 = value2[0:10]
    if isinstance(value1, str) and isinstance(value2, str):
        d2 = datetime.datetime.strptime(value1, '%Y-%m-%d')
        # Data inicial
        d1 = datetime.datetime.strptime(value2, '%Y-%m-%d')
        # Realizamos o calculo da quantidade de dias
        days = abs((d2 - d1).days)
        return days
