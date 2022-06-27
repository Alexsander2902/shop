#https://accounts.google.com/DisplayUnlockCaptcha
#https://myaccount.google.com/lesssecureapps
import smtplib
import ssl
from email.mime.text import MIMEText
#https://docs.python.org/3/library/email.mime.html#email.mime.multipart.MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from email.utils import make_msgid

import json

def send_email(credentials={}, \
    to=['testedeenvio@credihabitar.com.br'],
    cc=['testedeenvio@credihabitar.com.br'],
    bcc=['testedeenvio@credihabitar.com.br'],
    subject='subject',
    message='oi html',
    alt_message='oi',
    attachments={}):
    function_response = {}
    function_response['status'] = False
    function_response['content'] = ''
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)# 	25, 465 or 587 
        server.login(credentials['email'], credentials['senha'])
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = credentials['email']
        msg["To"] = to[0]
        msg["Cc"] = cc[0]
        #msg['Date'] = formatdate(localtime=True)
        #msg['Message-ID'] = make_msgid()
        #msg.preamble = 'This email has been automatically sent by credihabitar'
        msg.attach(MIMEText(alt_message, 'plain')) #, 'utf_8' #, _charset='UTF-8' # 'text/html'
        msg.attach(MIMEText(message, 'html'))
        for fname in attachments:
            msg.attach(MIMEApplication(attachments[fname], Content_Disposition='attachment; filename="%s"' % fname, Name=fname))
        #for file_path in ['./Dockerfile', './utils/teste.html',]: #dependendo da extensao nao pega (ex: __init__.py) e .html sobre escreve
        #    fname = os.path.basename(file_path)
        #    msg.attach(MIMEApplication(open(file_path, 'rb').read(), Content_Disposition='attachment; filename="%s"' % fname, Name=fname))
        
        server.sendmail(credentials['email'], to + cc + bcc, msg.as_string())
        function_response['status'] = True
    except Exception as error:
        print('Error send_email: ',str(error))
        function_response['content'] = str(error)
    return function_response


#server.set_debuglevel(1)
#server.sendmail(...)
##
#mail_server = smtplib.SMTP(...)
#mail_server.starttls()
