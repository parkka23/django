import peewee
from models import Category, Product
from insert_data import add_category, add_product
from retrieve import find_all_products, find_all_categories
choice='y'
def main():
    print('Hello, user! You have access to following functions:')
    print('\t1 - show categories\n\t2 - show products\n\t3 - add categoty\n\t4 - add product\n\t5 - delete category\n\t6 - delete product\n\t7 - update product')

    try:
        var=int(input('Enter your choice: '))
    except:
        print('You have to enter a number!')
        main()

    # categories
    if var==1:
        categories=find_all_categories()
        for i in categories:
            print(i.name)

    # prodects
    elif var==2:
        try:
            cat=int(input('Enter category (1 - dress, 2 - jeans, 3 - t-shirt, 4 - shoes, 5 - hat, 10 - cars, 12 - phones): '))
            categories=find_all_categories()
            products=find_all_products()

            for i in products:
                # print(x.category) # category id
                if i.category == categories[cat-1]:
                    print(f'{i.title}\t{i.price}\t{i.category}')
        except ValueError:
            print('You have to enter a number!')

    # add category
    elif var==3:
        name=input('Enter category: ')
        add_category(name)

    # add product
    elif var==4:
        title=input('Enter title: ')
        price=float(input('Enter price: '))
        category_name=input('Enter category: ')
        add_product(title,price,category_name)

    # delete category
    elif var==5:
        try:
            id=int(input('Enter category id: '))
            category=Category.get(category_id=id)
            name=category.name
            category.delete_instance()
            print('Category',name,'deleted')
        except Exception as e:
            print(f'Oops, we caught {e} error!')

    # delete product
    elif var==6:
        try:
            id=int(input('Enter product id: '))
            product=Product.get(product_id=id)
            title=product.title
            product.delete_instance()
            print('Product',title,'deleted')
        except Exception as e:
            print(f'Oops, we caught {e} error!')
        
    # update product
    elif var==7:
        id=int(input('Enter product id: '))
        option=int(input('Choose an oprion (1 - title, 2 - price): '))

        if option==1:
            t=input('Enter title: ')
            query=Product.update(title=t).where(Product.product_id==id)
            query.execute()
            # print(Product.get(product_id=id).title)
        elif option==2:
            price=input('Enter title: ')
            query=Product.update(price=price).where(Product.product_id==id)
            query.execute()
            # print(Product.get(product_id=id).title,Product.get(product_id=id).price,Product.get(product_id=id).category)
        
    else: print('Invalid option!')



    print('Do you want to continue? (y/n)')
    choice=input()

    if choice=='y':
        main()

main()