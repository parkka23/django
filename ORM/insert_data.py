import peewee
from models import Category, Product

def add_category(name):
    try:
        row=Category(name=name.lower().strip())
        row.save()
        print(f'Category { name.lower().strip() } is saved successfully.')
    except (peewee.IntegrityError, peewee.InternalError):
        print(f'Category {name.lower().strip()} already exist.')


# add_category('Dress')
# add_category('Jeans')
# add_category('  T-shirt')
# add_category('Shoes')
# add_category('  Hat ')

def add_product(title,price,category_name):
    try:
        category=Category.select().where(Category.name==category_name.lower().strip()).get()
        category_exists=True
    except peewee.DoesNotExist:
        category_exists=False

    if category_exists:
        row=Product(title=title.lower().strip(),price=price,category=category)
        row.save()
        print(f'Product {title.lower().strip()} is saved successfully.')
    else:
        print(f'Category {category_name.lower().strip()} does not exists.')


# add_product('zara dress',15000.50,'dress',)
# add_product('DG dress', 20500.30,'dress')
# add_product('supreme t-shirt',70000,'t-shirt')
# add_product('armany jeans',30000,'jeans')
# add_product('nike air',24000,'sneackers')

# select * from products join categories on (products.category_id=categories.category_id);

# python3 file.py