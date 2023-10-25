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
from datetime import datetime


def check_expire_data(product) -> bool:
    '''Функція для перевірки чи ще термін придатності дійсний'''
    expire_date = datetime.strptime(product.expdate, "%d/%m/%Y")
    present = datetime.now()
    if expire_date.date() > present.date():
        print("Next product:")
        x = True
    else:
        print("Your product has expired")
        x = False
    return x


#Список в якому будуть зберігатися продукти
products = []


#Об'єкт продукт
class Product:
    def __init__(self, ptype, pname, price, expdate, pcode):
        self.type = ptype
        self.name = pname
        self.price = price
        self.expdate = expdate
        self.code = pcode


while True:
    name = input("Enter product name (or 'exit' to finish): ")
    if name.lower() == 'exit':
        break
    product_type = input("Enter product type: ")
    price = input("Enter product price: ")
    code = random.randrange(10000000, 99999999)
    expdate = input("What is your product's expire date? (type it like this 15/10/2025): ")
    product = Product(name, product_type, price,expdate,code)
    try:
        if check_expire_data(product):
            products.append(product)
    except Exception:
        print("Expire date was redeemed incorrectly")
print("Here is a list of products:")
for product in products:
    print(f"Name: {product.name}, Type: {product.type}, Price: {product.price}, Product will expire {product.expdate}, Code: {product.code}")
