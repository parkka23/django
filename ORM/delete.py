import peewee
from models import Category, Product

# 1 СПОСОБ delete_instance без execute
# p1=Product.get(product_id=1)
# print(p1.title)
# p1.delete_instance()

# p1=Product.get(product_id=1) # IndexError
# print(p1) 


# 2 СПОСОБ WHERE EXECUTE
# products=Product.delete().where(Product.product_id>4)
# products.execute()
# print(list(Product.select())) # [<Product: 2>, <Product: 3>, <Product: 4>]

c=Category.get(name='dress')
print(c) # id 1
print(c.name) # dress
print(c.products) # sql 
print(list(c.products)) # [<Product: 2>]

