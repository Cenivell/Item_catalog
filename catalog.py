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
#
# Етап 2.
# З підключенням до бази даних зберігати всі введені користувачем айтеми у базі.
# Струкутра таблиці повинна відповідати атрибутам відповідного класу, а саме збереження релазуовуватись лише на останньому етапі, коли система відповідно буде мати весь список необхідного для зберігання.
# Зв'язок з базою для синхронізації клас/таблиця варто реалізувати на класі кожного item.
# Важливо, щоб система також пееревіряла наявність підключення, а також за потреби створювала всі необіхдін для збереження таблиці
# Частину з'єдання з базою можна вивести у окремий файл, і реалузвати за домогою engine у бібліотеці SQLAlchemy.
#
###########################
# Рішення нижче
###########################

from datetime import datetime

#Список в якому будуть зберігатися продукти
products = []


class Products:
    '''Батьківський клас продуктів'''
    def __init__(self, pname, price, pcode):
        self.name = pname
        self.price = price
        self.code = pcode

    def check_expire_data(self) -> bool:
        '''Функція для перевірки чи ще термін придатності дійсний'''
        expire_date = datetime.strptime(self.expdate, "%d/%m/%Y")
        present = datetime.now()
        if expire_date.date() > present.date():
            print("Next product:")
            x = True
        else:
            print("Your product has expired")
            x = False
        return x

    def add_products_to_the_database(connection):
        '''Функція для виписування продуктів в базу даних'''
        try:
            with connection.cursor() as cursor:
                for product in products:
                    # Вивів срок придатності продукта в змінну для того щоб можна було нормально перевірити, чи присутній срок придатності в продукті
                    expdate_info = product.expdate if hasattr(product, 'expdate') else None
                    if expdate_info is not None:
                        expdate_info_str = f"'{expdate_info}'"
                    else:
                        expdate_info_str = "NULL"
                    cursor.execute(
                        f"""INSERT INTO item_catalog (code, name, price, unit_of_measurement, expire_date, type) VALUES
                        ({product.code}, '{product.name}', {product.price}, '{product.unit_of_measurement}', {expdate_info_str}, '{product.product_type}');"""
                    )
                print("Data was successfully inserted to the database")
        except Exception as e_:
            print("An error occurred while inserting values into the database ", e_)

    def write_products_from_the_database_into_a_txt_file(file, connection):
        '''Функція для виписування продуктів в файл'''
        with open(file, 'a') as file:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM item_catalog;")
                    rows = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]
                for row in rows:
                        for i in range(len(row)):
                            file.write(f"{column_names[i]}: {row[i]}; ")
                        file.write("\n")
            except Exception as ex_:
                print("An error occurred while trying to write the database into a txt file ", ex_)


# Підкласи продуктів
class Fruits(Products):
    '''Клас фруктів'''
    def __init__(self, name, price, code):
        self.product_type = "Fruits"
        self.unit_of_measurement = "Kg"
        super().__init__(name, price, code)


class Vegetables(Products):
    '''Клас овочів'''
    def __init__(self, name, price, code):
        self.product_type = "Vegetables"
        self.unit_of_measurement = "Kg"
        super().__init__(name, price, code)


class CannedGoods(Products):
    '''Клас консервованих виробів'''
    def __init__(self, name, price, code, expdate):
        self.product_type = "Canned goods"
        self.unit_of_measurement = "Item"
        self.expdate = expdate
        super().__init__(name, price, code)


class Sweets(Products):
    '''Клас солодощів'''
    def __init__(self, name, price, code, expdate):
        self.product_type = "Sweets"
        self.unit_of_measurement = "Kg"
        self.expdate = expdate
        super().__init__(name, price, code)


class BreadGoods(Products):
    '''Клас хлібних виробів'''
    def __init__(self, name, price, code):
        self.product_type = "Bread goods"
        self.unit_of_measurement = "Item"
        super().__init__(name, price, code)
