from dbtools import row_map
from persistence import *

map()

def print_activity():
    print("Activities:")
    for activity in repo.activities.find_all():
        print(activity)


def print_branches():
    print("Branches:")
    for branch in repo.branches.find_all():
        print(branch)

def print_employees():
    print("Employees:")
    for employee in repo.employees.find_all():
        print(employee)

def print_products():
    print("Products:")
    for product in repo.products.find_all():
        print(product)



def print_Employees_Report():
    print("Employees Report:")
    mapEmpToSales = {}
    for row in repo.getEmployeeSaleSalary():
        map[row[0]] = row[1]

    for emp in repo.getSortedEmployees():
        totalSalary = emp.salary + mapEmpToSales.get(emp.name)
        print(f'{emp.name} + {totalSalary} + {emp.location}' )

def main():
    #TODO: implement
    print_activity()
    print_branches()
    print_employees()
    print_products()


    pass

if __name__ == '__main__':
    main()