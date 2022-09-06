from itertools import product
import peewee
from insert_data import add_category, add_product
from models import Category

#-------------cars------------

# добавляем категорию
# add_category('cars')

# из файла в список
# default 'r'
# with open('cars.txt','r') as file:
#     ls=file.readlines()
#     print(ls)

# убираем \n
# for i in ls:
#     car=i.replace('\n','')
#     add_product(car,1,'cars')

# вытаскиваем категорию
# category=Category.get(name='cars')

# принтим машины
# # related_name
# for i in category.products:
#     print(i.title)

#---------------- telefon-------

from random import randint
add_category('phones')
with open('telefon.txt') as file:
    ls=file.readlines()

for i in ls:
    title=i.replace('\n','')
    price=randint(1,1000)
    add_product(title,price,'phones')