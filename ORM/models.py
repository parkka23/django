from email.policy import default
from enum import unique
import peewee
from main import db
from datetime import datetime

# описание таблиц, их нахвания, поля
class BaseModel(peewee.Model):
    created_at=peewee.DateTimeField(default=datetime.now())
    class Meta:
        database=db

class Category(BaseModel):
    # автоинкримент, уникальный id
    category_id=peewee.PrimaryKeyField(null=False)
    name=peewee.CharField(max_length=100,unique=True)
   
    # описание доп настроек
    class Meta:
        db_table='categories'
        order_by=('created_at',)

class Product(BaseModel):
    product_id=peewee.PrimaryKeyField(null=False)
    title=peewee.CharField(max_length=100)
    # числа с плавающей точкой точнее float
    price=peewee.DecimalField(max_digits=10,decimal_places=2,default=None)
    # related_name - поле, через к можно вытащить, для обратной связи, через category можно вытащить products
    category=peewee.ForeignKeyField(Category,related_name='products',to_field='category_id',on_delete='cascade')
    
    class Meta:
        db_table='products'
        order_by=('created_at',)   

db.connect()
# Category.create_table()
# Product.create_table()

'''
\c orm_db
'''
