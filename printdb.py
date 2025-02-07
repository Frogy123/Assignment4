from dbtools import row_map
from persistence import *

map()

def print_activity():
    toPrint = repo.execute_query("""SELECT Activities.date, Activities.activator_id, Activities.quantity, Activities.product_id FROM Activities """)
    toPrint = repo.activities.find_all();
    print("Activities:\n" + toPrint)

def print_branches():
    toPrint = repo.execute_query("""SELECT Branches.location, Branches.number_of_employees, Branches.id FROM Branches """)
    print("Branches:\n" + toPrint)

def print_employees():
    toPrint = repo.execute_query("""SELECT Employees.name, Employees.salary, Employees.location,  Employees.id FROM Employees """)    print("Employees:\n" + toPrint)

def print_products():
    toPrint = repo.execute_query("""SELECT Products.description, Products.price ,Products.quantity, Products.id FROM Products """)
    print("Products:\n" + toPrint)

def print_Employees_Report():

def main():
    #TODO: implement
    print_activity()
    print_branches()
    print_employees()
    print_products()


    pass

if __name__ == '__main__':
    main()