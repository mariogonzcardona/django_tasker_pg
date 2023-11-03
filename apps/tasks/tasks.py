from django.template.loader import render_to_string 
from decouple import config
import threading
import smtplib
from email.mime.text import MIMEText
from django_tasker.settings.local import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL

def send_email_smtp(data):
    try:
        # print(data['to_email'])
        email_host= EMAIL_HOST
        email_port= EMAIL_PORT
        email_use_tls= EMAIL_USE_TLS
        email_host_password= EMAIL_HOST_PASSWORD
        
        email_host_user = config('EMAIL_HOST_USER')
        html_template = '../templates/send_email.html'
        html_message = render_to_string(html_template, data)
        
        # Crear el correo electrónico
        msg = MIMEText(html_message, "html","utf-8")
        msg['Subject'] = data['email_subject']
        msg['From'] = email_host_user
        msg['To'] = ', '.join(data['to_email'])
        
        # # Establecer la configuración del servidor de correo electrónico y enviar el correo
        
        # Establecer la configuración del servidor de correo electrónico y enviar el correo
        with smtplib.SMTP(email_host, email_port) as server:
            if email_use_tls:
                server.starttls()
            # solo autenticarse si la contraseña no está vacía
            if email_host_password:
                server.login(email_host_user, email_host_password)
            server.send_message(msg)
        print('Email sent successfully')
    except Exception as e:
        print(e)
        print('Email not sent')

def send_email_in_thread(data):
    # Crea un hilo y pasa la función send_email como objetivo (target)
    thread = threading.Thread(target=send_email_smtp, args=(data,))
    thread.start()
    print('Email sending process started in a separate thread')
    # En este punto, la función send_email se está ejecutando en el hilo separado

def send_notification_email(**kwargs):
    
    email_list=[]
    text=''
    email_subject=''
    
    # Validamos el action_type
    if kwargs['action_type'] == 'crear_tarea':
        
        text = f'El usuario {kwargs["full_name"]} ha creado una nueva tarea.'
        email_subject = 'Creacion de Tarea'
        email_list.append(kwargs["user_email"]) # Agregamos el correo del propio usuario
        
    elif kwargs['action_type'] == 'actualizcion_tarea':
        
        text = f'El usuario {kwargs["full_name"]} ha modificado una tarea.'
        email_subject = 'Actualizacion de Tarea'
        email_list.append(kwargs["user_email"]) # Agregamos el correo del propio usuario
        
    elif kwargs['action_type'] == 'eliminacion_tarea':
        
        text = f'El usuario {kwargs["full_name"]} ha eliminado una tarea.'
        email_subject = 'Eliminacion de Tarea'
        email_list.append(kwargs["user_email"]) # Agregamos el correo del propio usuario
    
    else:
        print("Algo ocurrio no se ejecuto ninguna accion")
    
    data = {
        'to_email': email_list,
        'email_subject': email_subject,
        'text': text,
    }
    send_email_in_thread(data)


