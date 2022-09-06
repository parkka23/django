'''
Виртуальное окружение - изолированная среда, куда устанавливаются библеотеки
у библеотек есть версии

1 прект одна версия
2 проект другая версия
будет конфликт

для каждого проекта надо создать свое виртуальное окружение, чтобы не было конфликтов


1. Установить venv:
sudo apt install python3 -venv

2. Создать в окр:
python3 -m venv venv

3. Активировать в окр:
source venv/bin/activate или . venv/bin/activate

4. Установить библеотеки рекурсивно (по очереди):
pip install -r requirements.txt

5. Просмотр установленных библеотек:
pip freeze 

6. Перенести в файд инфу об установленных библеотеках
pip freeze > requirements.txt

7. deactivate

peewee подключаться к базе данных
ORM (object-relational mapping) (объектно-реляционное отображение)технология программирования, благодаря которой разрабы могут использовать 
язык программирования для взаимодействия с реляционной базой данных (Postgres, MySQL), вместо написания операторов SQL
Это очень сильно ускоряет разработку приложения и базы данных, особенно на начальных этапах разработки 
(база д пустая, надо заполнять очень большим кол-вом данных)

python3 -m venv venv
. venv/bin/activate
touch req.txt

nano req.txt
peewee==3.14.4
psycopg2-binary==2.8.6 ctrl s ctrl x
pip install -r req.txt

touch models.py insert_data.py retrieve.py main.py
'''

from peewee import PostgresqlDatabase

db=PostgresqlDatabase(
    'orm_db',
    user='humster',
    password='1',
    host='localhost', # локально на ноуте
    port=5432 # postgres
)




