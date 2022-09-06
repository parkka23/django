'''
1. Создать виртуальное окружение 
    python3 -m venv venv

2. Устанавоиваем нужные библеотеки и django
    pip install <name>

3. Созадть директорий проекта и файл manage.py
    django-admin startproject <name> .

4. Создать приложение для проекта
    python3 manage.py startapp <name>
    django-admin startapp <name>
    ./manage.py startapp 

5. Закинуть в настройки Installed apps

6. Работать с проектом

--------

Проведение миграций:
1. Создать файлы миграций
    python3 manage.py makemigrations
    ./manage.py makemigrations

2. Исполнение файлов миграций (изменения в базу данных)
    python3 manage.py migrate

3. Создать суперюзера
    python3 manage.py createsuperuser 
    ./manage.py createsuperuser
'''