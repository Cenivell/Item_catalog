import main
import os


def print_products():
    '''Функція для виписування продуктів в консоль'''
    for product in main.products:
        # Вивів срок придатності продукта в змінну для того щоб могти нормально перевірити чи присутній срок придатності в продукті
        expdate_info = f" Expire data: {product.expdate}" if hasattr(product, 'expdate') else ""
        print(f"Type: {product.product_type} Name: {product.name} Price: {product.price} {expdate_info} Code: {product.code}")


def write_products():
    '''Функція для виписування продуктів в файл'''
    for product in main.products:
        # Вивів срок придатності продукта в змінну для того щоб могти нормально перевірити чи присутній срок придатності в продукті
        expdate_info = f" Expire data: {product.expdate}" if hasattr(product, 'expdate') else ""
        file.write(f"\nType: {product.product_type} Name: {product.name} Price: {product.price} {expdate_info} Code: {product.code} ")


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
        product = main.Fruits(name, price)
        main.products.append(product)
    elif product_type == '2':
        price = f'{input("Enter product price per kilo: ")} per kilo'
        product = main.Vegetables(name, price)
        main.products.append(product)
    elif product_type == '3':
        price = f'{input("Enter product price per item: ")} per item'
        expdate = input("What is your product's expire date? (type it like this 15/10/2025): ")
        product = main.CannedGoods(name, price, expdate)
        try:
            if main.check_expire_data(product):
                main.products.append(product)
        except Exception:
            print("Expire date was redeemed incorrectly")
    elif product_type == '4':
        price = f'{input("Enter product price per kilo: ")} per kilo'
        expdate = input("What is your product's expire date? (type it like this 15/10/2025): ")
        product = main.Sweets(name, price, expdate)
        try:
            if main.check_expire_data(product):
                main.products.append(product)
        except Exception:
            print("Expire date was redeemed incorrectly")
    elif product_type == '5':
        price = f'{input("Enter product price per item: ")} per item'
        product = main.BreadGoods(name, price)
        main.products.append(product)

print("Here is a list of products that you created:")
print_products()

print("Do you wish to write them into a .txt file")
answer = input("type Y or N ").lower()
if answer == "y":
    print("Do you wish to use manual directory input? If not then script's directory will be used")
    answer = input("type Y or N ").lower()
    if answer == "y":
        file_directory = input("Please redeem the directory of the file you are going to use (example D:\list\goods) ")
        file = f'{file_directory}.txt'
    elif answer == "n":
        file_directory = os.getcwd()
        file_name = input("Please redeem your file's name ")
        file = f'{file_directory}\{file_name}.txt'
    else:
        print("You have to print either Y or N")
        exit(0)
    with open(file, 'a') as file:
        write_products()
elif answer == "n":
    print("Terminated")
    exit()
