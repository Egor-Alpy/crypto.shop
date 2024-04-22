# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
import sqlite3 as sq

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
            user_id TEXT PRIMARY KEY,
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
                        promo TEXT,
                        discount INTEGER,
                        transaction_hash TEXT,
                        purchased REAL,
                        refer_code TEXT,
                        status TEXT,
                        data_time TEXT
                        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS promos (
                    promo TEXT PRIMARY KEY,
                    discount REAL,
                    quantity INTEGER
                    )""")

    # добавление промокода в базу данных
    def add_promo(self, promo: str, discount: int, quantity: int):
        edit_database(f"INSERT INTO promos ('promo', 'discount', 'quantity') VALUES ('{promo}', {discount}, {quantity})")

    # удаление промокода из базы данных
    def del_promo(self, name:str):
        edit_database(f"DELETE FROM promos WHERE promo = '{name}'")

    # добавление данных о совершенной покупке
    def add_purchase(self, user_id: int, username: str, user_github: str, soft_name: str, soft_price: float,
                     promo: str, discount: int, purchased: int, transaction_hash: str, refer_code: str, status: str, data_time: str):
        edit_database(f"INSERT INTO purchases ('user_id', 'username', 'user_github', 'soft_name', 'soft_price', "
                      f"'promo', 'discount', 'purchased', 'transaction_hash', 'refer_code', 'status', 'data_time') VALUES "
                      f"('{user_id}', '{username}', '{user_github}', '{soft_name}', '{soft_price}', '{promo}', "
                      f"'{discount}', '{purchased}', '{transaction_hash}', '{refer_code}', '{status}', '{data_time}')")

    # добавление нового пользователя в Базу Данных
    def adduser(self, user_id: int, name: str, message):
        edit_database(
            f"INSERT INTO users('user_id', 'name', 'refer_id') VALUES({user_id}, '{name}', '{message.text[7::]}')")

    # добавление нового софта в Базу Данных
    def addsoft(self, name: str, desc: str, price: float):
        edit_database(f"INSERT INTO software('name', 'description', 'price') VALUES('{name}', '{desc}', '{price}')")

    # удаление софта из Базы Данных
    def delsoft(self, name: str):
        edit_database(f"DELETE FROM software WHERE name = '{name}'")

    # добавление нового партнера в Базу Данных
    def addpartner(self, user_id: int, name: str, promocode: str, discount: int, quantity: int):
        edit_database(
            f"INSERT INTO partners('user_id', 'name', 'promocode', 'discount', 'quantity') VALUES('{user_id}', '{name}', '{promocode}', '{discount}', '{quantity}')")

    # удаление партнера из Базы Данных
    def delpartner(self, user_id: int):
        edit_database(f"DELETE FROM partners WHERE user_id = '{user_id}'")

    # извлечение информации из Базы Данных о выбранном софте
    def select_software_info(self, name: str):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute(f"SELECT name, description, price FROM software WHERE name = '{name}'")
            rows = cur.fetchall()
            return rows

    def select_refer_code(self, user_id):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute(f"SELECT refer_id FROM users WHERE user_id = '{user_id}'")
            row = cur.fetchone()
            return row

    def select_promo(self, promo):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute(f"SELECT promo, discount, quantity FROM promos WHERE promo = {promo}")
            row = cur.fetchone()
            return row

    def select_promos(self, all=False):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute("SELECT promo, discount, quantity FROM promos")
            rows = cur.fetchall()
            if all:
                return rows
            else:
                promos_list = []
                for i in range(len(rows)):
                    promos_list.append(rows[i][0])
                return promos_list

    def select_promo_discount(self, promo):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute(f"SELECT discount FROM promos WHERE promo = '{promo}'")
            row = cur.fetchone()
            return float(row[0])

    def select_promo_quantity(self, promo):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute(f"SELECT quantity FROM promos WHERE promo = '{promo}'")
            row = cur.fetchone()
            return float(row[0])

    def edit_promo_quantity_minus_one(self, promo, qty):
        with sq.connect(db_name) as con:
            cur = con.cursor()

            cur.execute(f"UPDATE promos SET quantity = '{qty}' - 1 WHERE promo = '{promo}'")

    def select_tx_hashes(self):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute(f"SELECT transaction_hash FROM purchases WHERE status = 1")
            rows_tuples = cur.fetchall()
            rows = []
            for i in range(len(rows_tuples)):
                rows.append(rows_tuples[i][0])
            return rows
