""" misc.py """

# Other Libraries
import os
import json

# Webserver
from flask import flash, request, redirect
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import make_response

# Models
from app.models import credentials
from app.models.misc import execute_query_activity_logs_get

# Utils
from app.utils.util import check_uuid
from app.utils.util import check_header
from app.utils.util import insert_file_log
from app.utils.util import formatter_datetime

# Controllers
from app.controllers import key
from app.controllers import check_session
from app.controllers.logs import create_log

from app.utils.util import load_file
from app.utils.util import save_file

from cryptography.fernet import Fernet

encryption = json.loads(load_file(file='./constants/encryption.json'))
f = Fernet(bytes(encryption['encryption'], 'utf-8'))
#key = Fernet.generate_key()
#bytes(str(key).split("'")[1], 'utf-8') == key

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx'}
UPLOAD_FOLDER = './uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def endpoint_upload(table, id, name):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        #file = request.files['file']
        file = request.files['file'].read()
        if request.files['file'].filename == '':
            flash('No selected file')
            return redirect(request.url)
        if request.files['file'] and allowed_file(request.files['file'].filename):
            filename = secure_filename(request.files['file'].filename)
            if not os.path.exists(UPLOAD_FOLDER + '/' + table + '/' + id):
                os.makedirs(UPLOAD_FOLDER + '/' + table + '/' + id)
            #atualmente sobreescreve se tiver o nome igual
            #habilitar lista dos arquivos anexados (mostrar arquivos da pasta)
            #mudar modo visualização e download de acordo com extensao
            #nao pode ter 2 arquivos mesmo nome no mesmo id
            #definir o que é nome renomeado do sandro?
            #colocar data e hora no arquivo?
            #file.save(os.path.join(UPLOAD_FOLDER + '/' + table + '/' + id, filename))
            save_file(file=os.path.join(UPLOAD_FOLDER + '/' + table + '/' + id, filename), content=str(f.encrypt(file)))
            return redirect(request.url)
    if request.method == 'GET':
        if 'tem_permissao':
            if os.path.isfile(UPLOAD_FOLDER + '/' + table + '/' + id + '/' + name):
                #return send_from_directory(os.getcwd() + '/' + UPLOAD_FOLDER[2:] + '/' + table + '/' + id, name)
                str_bin_content = load_file(os.getcwd() + '/' + UPLOAD_FOLDER[2:] + '/' + table + '/' + id + '/' + name).split("'")[1]
                bynary = f.decrypt(bytes(str_bin_content, 'utf-8'))
                response = make_response(bynary)
                extension = name.split(".")[-1]
                if extension == 'pdf':
                    response.headers['Content-Type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = \
                    'inline;' +name
                    return response
                elif extension =='jpg':
                    response.headers['Content-Type'] = 'image/jpeg'
                    # full_filename = os.path.join(UPLOAD_FOLDER, name)
                    return response
                elif extension =='png':
                    response.headers['Content-Type'] = 'image/png'
                    # full_filename = os.path.join(UPLOAD_FOLDER, name)
                    return response
                elif extension =='gif':
                    response.headers['Content-Type'] = 'image/gif'
                    # full_filename = os.path.join(UPLOAD_FOLDER, name)
                    return response
                elif extension == 'txt':
                    response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
                    # full_filename = os.path.join(UPLOAD_FOLDER, name)
                    return response
                else:
                    response.headers['Content-Type'] = 'application/'+extension
                    response.headers['Content-Disposition'] = \
                    'inline;'+name
                    return response
            else:
                return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form method=post enctype=multipart/form-data>
                <input type=file name=file>
                <input type=submit value=Upload>
                </form>
                '''

def endpoint_activity_logs_get():
    """ doctest for endpoint_activity_logs_get (pendent try exception global of function) without unit test
    """
    endpoint = 'endpoint_activity_logs_get'
    endpoint_response = {} 
    endpoint_response['status'] = False
    endpoint_response['content'] = None

    #try:
    if True:
        headers = dict(request.headers)
        check_header_response = check_header(header=headers,key=key)
        if check_header_response['status']:
            check_session_response = check_session(header=headers)
            if check_session_response['status']:
                input_validation_errors = not check_uuid(request.args.get('id'))
                query = {"response_type": request.args.get('response_type'), "id": request.args.get('id'), "search": request.args.get('search'), "order_column_1": request.args.get('order_column_1'), "order_direction_column_1": request.args.get('order_direction_column_1'), "limit": request.args.get('limit')}
                if not input_validation_errors:
                    execute_query_response = execute_query_activity_logs_get(query=query, credentials=credentials)
                    if execute_query_response['status'] or not request.args.get('id'):
                        if execute_query_response['content']:
                            if (len(execute_query_response['content']) == 1 and request.args.get('id')) or \
                                (len(execute_query_response['content']) >= 0 and not request.args.get('id')):
                                    
                                data = execute_query_response['content']
                                create_log(endpoint, 'activity_log', headers, data, query, ip= request.remote_addr)
                                return jsonify(data), 200
                            
                            else:
                                data = {'message': '500 Internal Server Error - Not found uniq'}
                                insert_file_log(function=endpoint, input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                                return jsonify(data), 500
                        else:
                            data = {'message': '500 Internal Server Error - Not found'}
                            insert_file_log(function=endpoint, input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                            return jsonify(data), 500
                    else:
                        data = {'message': '500 Internal Server Error - Error in connection or insert'}
                        insert_file_log(function=endpoint, input_function=['query: ',query,'execute_query_response: ',execute_query_response['content']])
                        return jsonify(data), 500
                else:
                    insert_file_log(function=endpoint, input_function=['query: ',query,'input_validation_errors: ',input_validation_errors])
                    return jsonify({"message": "500 Internal Server Error - Fields format error ("+str(input_validation_errors)+")"}), 500
            else:
                insert_file_log(function=endpoint, input_function=['headers: ',headers,'check_session_response: ',check_session_response['content']])
                return jsonify({"message": "403 Forbidden - "+check_session_response['content']}), 403
        else:
            insert_file_log(function=endpoint, input_function=['headers: ',headers,'check_header_response: ',check_header_response['content']])
            return jsonify({"message": "403 Forbidden - "+check_header_response['content']}), 403
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print('Error endpoint_activity_logs_get: ', exc_type, fname, exc_tb.tb_lineno, str(e))
