###########################
# Опис завдання:
# СПробужмо розробити просту програму для обілку складу у магазині.
# У завданні будемо детальніше розбирати можливості роботи класами, тому всі товари формуємо по принципах ООП (почитай за це додатково).
#
# Технічне завдання:
# На основі вхідних даних про наявність різних товарів у магазині
# Програма буде складатись з 2 файлів: один включатиме опис товарів, а інший - власне процес взаємодії з користувачем.
# 1) Товари.
# 	Кожен товар за своєю суттю є об'єктом. У магазині зустрічаються товари мінімум 5 типів - овочі, фрукти, консерви, солодощі, хліб (за бажанням, можеш додати ще пару інших типів).
# 	Далі кожен товар має власне свою специфікацію - нпариклад, овочі - це яблуко, груша, слива тощо.
# 	Всі вони мають мати тип, ціну, дату придатності та унікальний номер (штрихкод - робиш просто як рандомну стрічку з 8 восьми символів). Всі ніші атрибути можуть відрізнятися.
# 	Також має бути власне метод, чи переверія, чи строк придатності ще не вийшов.
# 	Зверни увагу, що програма має правильно обирати, який об'єкт створити за типом тоівару.
# 2) Взаємодія з користувачем.
# 	У цьому файлі прописуємо тільки параметри взаємодії з користувачем. Він має мати змогу занести якиїсь товар до системи (відповідно ініалізувтаи об'єкт з якимось параметрами).
# 	Користувач має мати змогу додати будь яку клькітсь товарів за один сеанс.
# 	Коли всі товари додані, система, за згодою корситувача, має зргенерувати йому вихідний файл зі списком всіх товарів, де відрбразиться: штрихкод, товар, ціна, та всі його інші характеристики.
# Використати тільки python та вбудовані бібліотеки.
# Вхідні параметри - за потребою клієнта

###########################
# Рішення нижче
###########################


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
    #Перевіряю чи правильно написана дата та чи срок годності дійсний
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
