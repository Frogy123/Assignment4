import sqlite3
import atexit

import dbtools
from dbtools import Dao
 
# Data Transfer Objects:
class Employee:
    def __init__(self, id: int, name: str, salary: float, branche: int):
        self.id = id
        self.name = name
        self.salary = salary
        self.branch = branche

    def __str__(self):
        return str([self.name, self.salary, self.branch, self.id])


class Supplier:
    def __init__(self, id: int, name: str, contact_information: str):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __str__(self):
        return str([self.name, self.contact_information, self.id])


class Product:
    def __init__(self, id: int, description: str, price: float, quantity: int):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return str([self.description, self.price, self.quantity, self.id])


class Branch:
    def __init__(self, id: int, location: str, number_of_employees: int):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def __str__(self):
        return str([self.location, self.number_of_employees, self.id])


class Activity:
    def __init__(self, product_id: int, quantity: int, activator_id: int, date: str):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def __str__(self):
        return str([self.date, self.activator_id, self.quantity, self.product_id])

#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self.employees = Dao(Employee, self._conn, 'employees')
        self.suppliers = Dao(Supplier, self._conn, 'suppliers')
        self.products = Dao(Product, self._conn, 'products')
        self.branches = Dao(Branch, self._conn, 'branches')
        self.activities = Dao(Activity, self._conn, 'activities')
        
 
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branch    INT REFERENCES branches(id)
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

    def getSortedEmployees(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM employees ORDER BY employees.name ASC')
        return dbtools.orm(c, Employee)

    def getEmployeeSaleSalary(self):
        return self.execute_command("""
            SELECT Employees.name, SUM(Products.price * Activities.quantity) 
            FROM Employees
            JOIN Activities ON Employees.id = Activities.activator_id
            JOIN Products ON Activities.product_id = Products.id
            GROUP BY Employees.name
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
 
# singleton
repo = Repository()
atexit.register(repo._close)