import os
import catalog
try:
    from psql_connection import connection
except Exception as ex:
    print("Failed while connecting to psql (try adjusting the psql connection config file). Error: ", ex)

# Checking if the table exists
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'item_catalog');")
        table_exists = cursor.fetchone()[0]
        # If table exists finding out what is the biggest code in the table to generate unique codes
        if table_exists:
            cursor.execute("""SELECT MAX(code) FROM item_catalog;""")
            code = cursor.fetchone()[0]
            # If the table exist but doesn't have any product set the code to 9999999
            if code is None:
                code = 9999999
            print(code)
        # If the table doesn't exist set the code to 9999999
        else:
            code = 9999999
except Exception as exc:
    print("Error while working with PSQL ", exc)

product_type = ""
while product_type != "0":
    product_type = input("Enter product type  (type '1' if Fruit, '2' if Vegetable, '3' if Canned good, '4' if Sweets, '5' if Bread goods, '0' if you wanna exit): ")
    if product_type == '0':
        pass
    elif product_type in map(str, range(1, 6)):
        name = input("Enter product name: ")
        code += 1
    else:
        print("Product type was redeemed incorrectly")
    if product_type == '1':
        price = input("Enter product price per kilo: ")
        product = catalog.Fruits(name, price, code)
        catalog.products.append(product)
    elif product_type == '2':
        price = input("Enter product price per kilo: ")
        product = catalog.Vegetables(name, price, code)
        catalog.products.append(product)
    elif product_type == '3':
        price = input("Enter product price per item: ")
        expdate = input("What is your product's expire date? (type it like this 15/10/2025): ")
        product = catalog.CannedGoods(name, price, code, expdate)
        try:
            if catalog.Products.check_expire_data(product):
                catalog.products.append(product)
        except Exception:
            print("Expire date was redeemed incorrectly")
    elif product_type == '4':
        price = input("Enter product price per kilo: ")
        expdate = input("What is your product's expire date? (type it like this 15/10/2025): ")
        product = catalog.Sweets(name, price, code, expdate)
        try:
            if catalog.Products.check_expire_data(product):
                catalog.products.append(product)
        except Exception:
            print("Expire date was redeemed incorrectly")
    elif product_type == '5':
        price = input("Enter product price per item: ")
        product = catalog.BreadGoods(name, price, code)
        catalog.products.append(product)


print("Do you wish to write the list into a database?")
answer = input("type Y or N ").lower()
if answer == "y":
        try:
            with connection.cursor() as cursor:
                # Check if the table exists
                if not table_exists:
                    # Table doesn't exist, so create it
                    cursor.execute(
                        """CREATE TABLE item_catalog(
                            code numeric(8,0) PRIMARY KEY,
                            name varchar(50) NOT NULL,
                            price numeric(16,2) NOT NULL,
                            unit_of_measurement varchar(10) NOT NULL,
                            expire_date DATE,
                            type varchar(30) NOT NULL);""")
                    print("A new table was successfully created")
                else:
                    print("Table already exists.")
        except Exception as e:
            print("An error occurred while trying to create a table: ", e)
        catalog.Products.add_products_to_the_database(connection)
elif answer == "n":
    print("Proceeding to the next step")
else:
    print("You had to print either Y or N. Proceeding to the next step")
print("Do you wish to write the database into a txt file??")
answer = input("type Y or N ").lower()
if answer == "y":
    print("Do you wish to use manual directory input? If not then script's directory will be used")
    answer = input("type Y or N ").lower()
    if answer == "y":
        file_directory = input("Please redeem the directory of the file you are going to use (example D:\list\goods) ")
        file = f'{file_directory}.txt'
        catalog.Products.write_products_from_the_database_into_a_txt_file(file, connection)
    elif answer == "n":
        file_directory = os.getcwd()
        file_name = input("Please redeem your file's name ")
        file = f'{file_directory}\{file_name}.txt'
        catalog.Products.write_products_from_the_database_into_a_txt_file(file, connection)
    else:
        print("You had to print either Y or N")
elif answer == "n":
    print("Terminated")
else:
    print("You had to print either Y or N")
if connection:
    connection.close()
    print("PostgreSQL connection was successfully closed")
