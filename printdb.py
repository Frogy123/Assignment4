from dbtools import row_map
from persistence import *



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
    for emp in repo.getEmployeesReport():
        print(f'{emp[0]} {emp[1]} {emp[2]} {emp[3]}')

def print_Activities_Report():
    print("Activities Report:")
    for act in repo.getActivitiesReport():
        print(act)

def main():
    #TODO: implement
    print_activity()
    print_branches()
    print_employees()
    print_products()

    print_Employees_Report()
    print_Activities_Report()


    pass

if __name__ == '__main__':
    main()