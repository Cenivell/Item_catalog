import os
import catalog
try:
    from psql_connection import connection, table_exists
except Exception as ex:
    print("Failed while connecting to psql (try adjusting the psql connection config file). Error: ", ex)


def edit_existing_product_value(new_value_name, code):
    new_value = input(f"Redeem a new product {new_value_name} ")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE item_catalog 
                SET {new_value_name}='{new_value}' 
                WHERE code='{code}'""")
    except Exception as e:
        print(f"Error while changing product {new_value_name}. ", e)


code = ""
answer = ""
while code != 0:
    try:
        code = int(input('Please redeem an 8-digit code of the product you want to add or edit (type "0" if you want to exit): '))
    except Exception:
        print("Make sure your code is 8-DIGIT")
    # Checking if a code meets the requirements
    if len(str(code)) == 8:
        if table_exists:
            try:
                with connection.cursor() as cursor:
                    # Checking if a redeemed code belongs to already existing product in the database
                    cursor.execute(f"""SELECT EXISTS(SELECT * FROM item_catalog WHERE code='{code}');""")
                    product_exists = cursor.fetchone()[0]
                     # If a product with the redeemed code already exists enter a product editor
                    if product_exists:
                        print("Product with the code you redeemed already exists.")
                        answer = input("If you want to edit it type '1', to delete it type '2', type '0' if you wanna use a new code ")
                        if answer == '1':
                            while answer != '0':
                                answer = input("Which value do you wish to edit? '1' - name, '2' - price, '3' - unit of measurement, '4' - expire data, '5' - type, '0' to exit ")
                                if answer == '1':
                                    edit_existing_product_value("name", code)
                                elif answer == '2':
                                    edit_existing_product_value("price", code)
                                elif answer == '3':
                                    edit_existing_product_value("unit_of_measurement", code)
                                elif answer == '4':
                                    edit_existing_product_value("expire_date", code)
                                elif answer == '5':
                                    edit_existing_product_value("type", code)
                                elif answer == '0':
                                    print("Exiting for product editor")
                                else:
                                    print("You have to type any digit from 0 to 5!")
                        elif answer == '2':
                            try:
                                with connection.cursor() as cursor:
                                       cursor.execute(f"""DELETE FROM item_catalog WHERE code='{code}';""")
                                print("Product was successfully deleted")
                            except Exception as e:
                                    print("Error while trying to delete a product. ", e)
                        elif answer == '0':
                            print("Exiting product editor")
                        else:
                            print("You had to print a digit from 0 to 2")
            except Exception as ex_:
                print("An error occurred while working with SQL ", ex_)
        if not product_exists:
            product_type = input("Enter product type  (type '1' if Fruit, '2' if Vegetable, '3' if Canned good, '4' if Sweets, '5' if Bread goods): ")
            if product_type in catalog.product_types_dict:
                name = input("Enter product name: ")
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
    elif code == 0:
        print("Proceeding to the next step")
    else:
        print("Code was redeemed incorrectly")


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
print("Do you wish to write the database into a txt file?")
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
