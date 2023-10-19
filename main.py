import random
import os
from datetime import datetime


def check_expire_data(x):
    expire_date = datetime.strptime(x.product_expdata, "%d/%m/%Y")
    present = datetime.now()
    if expire_date.date() > present.date():
        x.printname()
        print("Next product:")
    else:
        print("Your product has expired")


def write_value_to_the_catalog(ptype: str, name: str, price: str, expdata: str, code: str, catalog):
    '''Функція для того щоб виписувати продукт в файл'''
    catalog.write(str(f"Type:{ptype}   "))
    catalog.write(str(f"Name:{name}   "))
    catalog.write(str(f"Price:{price}   "))
    catalog.write(str(f"Expire data:{expdata}   "))
    catalog.write(str(f"Code:{code}    "))
    catalog.write("\n")


def add_new_item():
    '''Функція для додавання нового предмета/продукта в каталог'''
    code = random.randrange(10000000, 99999999)
    new_product = Product(input("What is your product's type? "), input("What is your product's name? "), input("What is your product's price? "), input("What is your product's expire data? (type it like this 15/10/2025) "), code)
    try:
        check_expire_data(new_product)
    except Exception:
        print("Expire date was redeemed incorrectly")


print("Welcome do u wish to use manual directory input? If not then script's directory will be used")
answer = input("type Y or N ").lower()

if answer == "y":
    file_directory = input("Please redeem the directory of the file that you wanna use (example D:\menu\drinks) ")
    file_name = os.path.basename(file_directory)
    file = f'{file_directory}.txt'

elif answer == "n":
    file_directory = os.getcwd()
    file_name = input("Please redeem your file's name ")
    file = str(f'{file_directory}\{file_name}.txt')
else:
    print("You have to print either Y or N")
    exit(0)


#Об'єкт продукт
class Product:
    def __init__(self, ptype, pname, price, expdate, pcode):
        self.product_type = ptype
        self.product_name = pname
        self.product_price = price
        self.product_expdata = expdate
        self.product_code = pcode

    def printname(self):
        with open(file, 'a') as catalog:
            write_value_to_the_catalog(self.product_type, self.product_name, self.product_price, self.product_expdata, self.product_code, catalog)


while True:
    add_new_item()
