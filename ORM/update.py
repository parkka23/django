from distutils.util import execute
import peewee
from models import Product

# products=Product.select()
# print(products) # SELECT "t1"."product_id", "t1"."created_at", "t1"."title", "t1"."price", "t1"."category_id" FROM "products" AS "t1"
# print(list(products)) # [<Product: 1>, <Product: 2>, <Product: 3>, <Product: 4>]

# p=Product.get(product_id=1)
# print(p) # 1
# print(p.title) # zara dress
# print(dir(p)) # methods

# 1 product
# query=Product.update(price=1).where(Product.product_id==1)
# query.execute()
# print(Product.get(product_id=1).price)

# all products
# query=Product.update(price=Product.price*2)
# query.execute()
# for i in Product.select():
#     print(f'{i}\t{i.title}\t{i.price}')


# ctrl l - поднять экран