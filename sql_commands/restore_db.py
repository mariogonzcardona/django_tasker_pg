from django.core.management import execute_from_command_line
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from psycopg2 import extensions
from decouple import config
from pathlib import Path
import psycopg2
import time
import os
import sys

project_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_path))
from django_tasker.settings.base import *

ENV_ROLE = config('ENV_ROLE', default='local')

DB_CONFIG = get_db_config()

DB_HOST = DB_CONFIG['HOST']
DB_PORT = DB_CONFIG['PORT']
DB_USER = DB_CONFIG['USER']
DB_PASSWORD = DB_CONFIG['PASSWORD']
DB_NAME = DB_CONFIG['NAME']

def delete_db():
    try:
        # Conéctate al servidor PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'  # Conéctate a la base de datos "postgres" para realizar la eliminación
        )
        
        # Establece el nivel de aislamiento en AUTOCOMMIT
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Crea la sentencia SQL para eliminar la base de datos
        drop_database_query = f"DROP DATABASE IF EXISTS {DB_NAME};"
        
        # Crea un cursor para ejecutar comandos SQL
        cursor = conn.cursor()

        # Ejecuta el comando para eliminar la base de datos
        cursor.execute(drop_database_query)

        # Confirma los cambios en la conexión
        conn.commit()

        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        print("-" * 20, "Deleted database successfully", "-" * 20, sep="")
    except Exception as e:
        print(e)

def create_db():
    try:
        # Conéctate al servidor PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        
        # Establece el nivel de aislamiento en AUTOCOMMIT
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        # Crea un cursor para ejecutar comandos SQL
        cursor = conn.cursor()

        # Crea la sentencia SQL para crear la base de datos
        create_database_query = f"CREATE DATABASE {DB_NAME};"

        # Ejecuta el comando para crear la base de datos
        cursor.execute(create_database_query)

        # Confirma los cambios en la conexión
        conn.commit()

        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        print("-" * 20, "Created database successfully", "-" * 20, sep="")
    except Exception as e:
        print(e)

def delete_migrations():
    apps_path = "apps"
    migrations_folder = "migrations"
    pycache_folder = "__pycache__"

    # Borra los archivos de migraciones y los archivos pycache
    for app in os.listdir(apps_path):
        app_path = os.path.join(apps_path, app)
        if os.path.isdir(app_path):
            migrations_path = os.path.join(app_path, migrations_folder)
            pycache_path = os.path.join(app_path, pycache_folder)
            if os.path.exists(migrations_path):
                for mig_file in os.listdir(migrations_path):
                    if mig_file != '__init__.py':
                        mig_file_path = os.path.join(migrations_path, mig_file)
                        os.system(f"rm -rf {mig_file_path}")
                        print(f"Removed migration file {mig_file_path}")
                print(f"Removed migrations folder for app {app}")
            if os.path.exists(pycache_path):
                os.system(f"rm -rf {pycache_path}")
                print(f"Removed pycache folder for app {app}")

def create_migrations():
    print("-" * 20, "Creating migrations", "-" * 20, sep="")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_tasker.settings.local')
    application = get_wsgi_application()

    from django.core.management import call_command

    call_command('makemigrations')
    call_command('migrate')
    call_command('loaddata', './fixtures/users.json')
    
def main():
    try:
        # # Proceso para eliminar la base de datos
        delete_db()
        time.sleep(2)
        
        # Proceso para crear la base de datos
        create_db()
        time.sleep(2)

        # Proceso para eliminar las migraciones
        delete_migrations()
        time.sleep(1)
        
        # Proceso para crear las migraciones
        create_migrations()
       
    except Exception as e:
        print(e)

# Generamos el metodo main
if __name__ == '__main__':
    # Ejecutamos el metodo main
    main()
