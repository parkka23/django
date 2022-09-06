import peewee
from models import Category, Product

def find_all_categories():
    return Category.select()

def find_all_products():
    return Product.select()

categories=find_all_categories()

# print(categories) # sql запрос

# print('Categories in BD:')
# for x in categories:
#     # print(x) # id
#     print(x.name)

# choice=int(input('Enter category (1 - dress, 2 - jeans, 3 - t-shirt, 4 - shoes, 5 - hat): '))

# products=find_all_products()

# for x in products:
#     # print(x.category) # category id
#     if x.category == categories[choice-1]:
#         print(x.title, x.price, x.category)

