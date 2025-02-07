import sqlite3
import atexit
from dbtools import Dao
 
# Data Transfer Objects:
class Employee:
    def __init__(self, id: int, name: str, salary: float, branche: int):
        self.id = id
        self.name = name
        self.salary = salary
        self.branche = branche

    def __repr__(self):
        return f"Employee(id={self.id}, name='{self.name}', salary={self.salary}, branche={self.branche})"


class Supplier:
    def __init__(self, id: int, name: str, contact_information: str):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __repr__(self):
        return f"Supplier(id={self.id}, name='{self.name}', contact_information='{self.contact_information}')"


class Product:
    def __init__(self, id: int, description: str, price: float, quantity: int):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(id={self.id}, description='{self.description}', price={self.price}, quantity={self.quantity})"


class Branche:
    def __init__(self, id: int, location: str, number_of_employees: int):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def __repr__(self):
        return f"Branche(id={self.id}, location='{self.location}', number_of_employees={self.number_of_employees})"


class Activitie:
    def __init__(self, product_id: int, quantity: int, activator_id: int, date: str):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def __repr__(self):
        return f"Activitie(product_id={self.product_id}, quantity={self.quantity}, activator_id={self.activator_id}, date='{self.date}')"

#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self.employees = Dao(Employee, self._conn, 'employees')
        self.suppliers = Dao(Supplier, self._conn, 'suppliers')
        self.products = Dao(Product, self._conn, 'products')
        self.branches = Dao(Branche, self._conn, 'branches')
        self.activities = Dao(Activitie, self._conn, 'activities')
        
 
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
 
# singleton
repo = Repository()
atexit.register(repo._close)