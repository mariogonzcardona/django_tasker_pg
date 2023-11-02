# Sistema Django-Tasker-PG

Este proyecto esta desarrollado para cubrir un conjunto de aplicaciones como:

- Tasks.
- Core.

Este proyecto utiliza el framework Django para el desarrollo de aplicaciones backend.

## Características

Antes de comenzar, asegúrate de tener instalado los siguientes requisitos en tu sistema:

- Python == 3.11.0
- Django == 4.2.3

## Instalacion

Siga los siguientes pasos para instalar y ejecutar este proyecto en su sistema local:

1.- Clone este repositorio en su sistema local:

```sh
git clone https://github.com/mariogonzcardona/django_tasker_pg.git
```

Es necesario crear la rama de `develop`, para poder hacer modificaciones, de lo contrario ejecutar software en la rama `main`

2.- Entra en la carpeta del proyecto para poder comenzar con la ejecución:
```sh
cd django_tasker_pg
```
3.-Antes de comenzar a instalar las dependencias, es necesario crear un ambiente virtual y activarlo:
### En Windows:
```sh
pip install virtualenv
```
```sh
virtualenv nombre_del_entorno
```
```sh
nombre_del_entorno\Scripts\activate
```
```sh
nombre_del_entorno\Scripts\deactivate
```
### En Linux y Mac:
```sh
pip install virtualenv
```
```sh
virtualenv nombre_del_entorno
```
```sh
source nombre_del_entorno/bin/activate
```
```sh
deactivate
```

4.-Instale las dependencias requeridas para el proyecto:
```sh
pip install -r requirements.txt
```

5.-Generar un archivo para las variables de entorno `.env` para establecer los parametros necesarios de acceso, utilizar `.env.example` como referencia.

6.-Inicie el servidor de desarrollo, asegurar que el servicio de PostgreSQL este encendido:
```sh
python manage.py runserver
```
7.- Al ejecutar el proyecto debera mostrar en consola un mensaje similar a este:
```sh
$ runserver 
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 1 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): auth.
Run 'python manage.py migrate' to apply them.
February 06, 2023 - 12:07:02
Django version 4.1.5, using settings 'settings.production'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Ahora, puedes acceder a la aplicación en http://localhost:8000/ en tu navegador.

## Configuración
Si necesitas hacer cambios en la configuración del proyecto, puedes editar el archivo settings.py en la carpeta del proyecto.

Para poder efectuar los cambios en Base de datos es necesario crear una BD con el nombre de `django_tasker_db`.

Posteriormente se deberán ejecutar los siguientes comandos para crear las tablas necesarias.
- Este comando generara los archivos necesarios para crear las tablas en BD.
```sh
python manage.py makemigrations
```
- Este comando generara las tablas en la BD de `django_tasker_db`.
```sh
python manage.py migrate
```


Para ingresar datos iniciales desde la terminal a la BD es necesario dirigirse a la carpeta de `fixtures`, en donde se localizan los archivos .json con los datos de prueba:
```sh
python manage.py loaddata fixtures/full_data_db.json
```

De esta forma ya tendras los valores iniciales para generar los CRUDs de Tasks, Users, y demas.

Para poder realizar un backup de la información en la BD, es necesario considerar el siguiente comando para caracteres especiales dentro de la información: 

```sh
python -Xutf8 ./manage.py dumpdata > db.json
```

## Documentación

Es necesario generar los archivos de documentación para poder visualizar los Endpoints de la API Swagger.
```sh
python manage.py collectstatic
```

Para poder tener acceso a los Endpoints de forma visual se puede acceder a la documentación de Swagger en el siguiente acceso. 
```sh
http://127.0.0.1:8000/swagger/
```

Si requieres tener acceso al administrador de Django, es necesario crear un Superusuario en consola:

```sh
python manage.py createsuperuser
```

Para acceder ingresar a la siguiente direccion:
```sh
http://127.0.0.1:8000/admin/
```