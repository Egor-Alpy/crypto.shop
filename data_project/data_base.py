# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
import sqlite3 as sq

from aiogram.types import InlineKeyboardMarkup,  InlineKeyboardButton

# название Базы Данных
db_name = "DB_CRYPTOFIL.db"


# запрос на редактирование в базу данных
def edit_database(request: str, db_name=db_name):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(request)


class DataBase:
    global db_name

    def __init__(self):
        pass
    # создание табличек Базы Данных
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            indexx INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            refer_id TEXT
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS software (
            indexx INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS partners (
            indexx INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            promocode INTEGER,
            discount INTEGER,
            quantity INTEGER
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS purchases (
                        indexx INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        username TEXT,
                        user_github TEXT,
                        soft_name TEXT,
                        soft_price INTEGER,
                        refer_id INTEGER,
                        refer_discount INTEGER,
                        promocode TEXT,
                        discount INTEGER,
                        total_discount INTEGER,
                        purchased INTEGER
                        )""")

    # добавление данных о совершенной покупке
    def addpurchase(self, user_id: int, username: str, user_github: str, soft_name: str, soft_price: float,
                    refer_id: int, refer_discount: int, promocode: str, discount: int,
                    total_discount: int, purchased: int):
        edit_database(f"INSERT INTO purchases ('user_id', 'username', 'user_github', 'soft_name', 'soft_price', "
                      f"'refer_id', 'refer_discount', 'promocode', 'discount', 'total_discount', 'purchased') VALUES "
                      f"('{user_id}', '{username}', '{user_github}', '{soft_name}', '{soft_price}', '{refer_id}', "
                      f"'{refer_discount}', '{promocode}', '{discount}', '{total_discount}', '{purchased}')")

    # добавление нового пользователя в Базу Данных
    def adduser(self, user_id: int, name: str, message):
        edit_database(f"INSERT INTO users('user_id', 'name', 'refer_id') VALUES({user_id}, '{name}', '{message.text[7::]}')")

    # добавление нового софта в Базу Данных
    def addsoft(self, name: str, desc: str, price: float):
        edit_database(f"INSERT INTO software('name', 'description', 'price') VALUES('{name}', '{desc}', '{price}')")

    # удаление софта из Базы Данных
    def delsoft(self, name: str):
        edit_database(f"DELETE FROM software WHERE name = '{name}'")

    # добавление нового партнера в Базу Данных
    def addpartner(self, user_id: int, name: str, promocode: str, discount: int, quantity: int):
        edit_database(f"INSERT INTO partners('user_id', 'name', 'promocode', 'discount', 'quantity') VALUES('{user_id}', '{name}', '{promocode}', '{discount}', '{quantity}')")

    # удаление партнера из Базы Данных
    def delpartner(self, user_id: int):
        edit_database(f"DELETE FROM partners WHERE user_id = '{user_id}'")

    # извлечение информации из Базы Данных о выбранном софте
    def select_software_info(self, name: str):
        with sq.connect("DB_CRYPTOFIL.db") as con:
            cur = con.cursor()
            cur.execute(f"SELECT name, description, price FROM software WHERE name = '{name}'")
            rows = cur.fetchall()
            return rows




