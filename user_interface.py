import catalog
import psycopg2
from psql_connection_config import host, user, db_name


def add_products_to_the_database():
    '''Функція для виписування продуктів в базу даних'''
    with connection.cursor() as cursor:
        for product in catalog.products:
            # Вивів срок придатності продукта в змінну для того щоб можна було нормально перевірити, чи присутній срок придатності в продукті
            expdate_info = product.expdate if hasattr(product, 'expdate') else ""
            cursor.execute(
                """INSERT INTO item_catalog (code, name, price, expire_date, type) VALUES
                (%s, %s, %s, %s, %s);""",
                (product.code, product.name, product.price, expdate_info, product.product_type)
            )
        print("Data was successfully inserted to the database")


product_type = ""
while product_type != "0":
    product_type = input("Enter product type  (type '1' if Fruit, '2' if Vegetable, '3' if Canned good, '4' if Sweets, '5' if Bread goods, '0' if you wanna exit): ")
    if product_type == '0':
        pass
    elif product_type in map(str, range(1, 6)):
        name = input("Enter product name: ")
    else:
        print("Product type was redeemed incorrectly")
    if product_type == '1':
        price = f'{input("Enter product price per kilo: ")} per kilo'
        product = catalog.Fruits(name, price)
        catalog.products.append(product)
    elif product_type == '2':
        price = f'{input("Enter product price per kilo: ")} per kilo'
        product = catalog.Vegetables(name, price)
        catalog.products.append(product)
    elif product_type == '3':
        price = f'{input("Enter product price per item: ")} per item'
        expdate = input("What is your product's expire date? (type it like this 15/10/2025): ")
        product = catalog.CannedGoods(name, price, expdate)
        try:
            if catalog.Products.check_expire_data(product):
                catalog.products.append(product)
        except Exception:
            print("Expire date was redeemed incorrectly")
    elif product_type == '4':
        price = f'{input("Enter product price per kilo: ")} per kilo'
        expdate = input("What is your product's expire date? (type it like this 15/10/2025): ")
        product = catalog.Sweets(name, price, expdate)
        try:
            if catalog.Products.check_expire_data(product):
                catalog.products.append(product)
        except Exception:
            print("Expire date was redeemed incorrectly")
    elif product_type == '5':
        price = f'{input("Enter product price per item: ")} per item'
        product = catalog.BreadGoods(name, price)
        catalog.products.append(product)


print("Do you wish to write the list into a database?")
answer = input("type Y or N ").lower()
if answer == "y":
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=input("Please redeem your database password (You can change other parameters such as database name, user and host inside the config file) "),
            database=db_name
        )

        connection.autocommit = True

        try:
            with connection.cursor() as cursor:
                 cursor.execute(
                     """CREATE TABLE item_catalog(
                         code INT PRIMARY KEY,
                         name varchar(50) NOT NULL,
                         price varchar(50) NOT NULL,
                         expire_date varchar(50),
                         type varchar(50) NOT NULL);"""
                 )
            print("A new table was successfully created")
        except Exception:
            pass
        add_products_to_the_database()
    except Exception as _ex:
        print("Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("PostgreSQL connection was successfully closed")
elif answer == "n":
    print("Terminated")
else:
    print("You had to print either Y or N")
