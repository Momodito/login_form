Para usar:
1) En una terminal, escribir "docker-compose up" (Sin las comillas) ¡Importante, asegurarse de tener instalado docker!
2) En otra terminal, ejecutar un entorno virtual (Recomendacion: Buscar documentacion de Virtualenv)
3) Habiendo iniciado el entorno virtual, escribir en otra terminal "pip install -r requirements.txt" (Sin las comillas)
4) Cuando se instalen los requerimientos, escribir en esa misma terminal "python manage.py makemigrations" (Sin las comillas)
5) En la misma terminal, escribir "python manage.py migrate" (Sin las comillas)
6) En la misma terminal, escribir "python manage.py runserver" (Sin las comillas) y acceder a localhost:8000

Listo, disfrute de su página web. Puede registrar usuarios e iniciar sesion.

NOTA: Para gestionar la base de datos PostgreSQL, debe descargar PgAdmin, iniciar la conexión con las credenciales de abajo:
        'NAME': 'database_login',
        'USER': 'db_login',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',