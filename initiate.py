from persistence import *

import sys
import os



def add_branch(splittedline : list[str]):
    #TODO: add the branch into the repo
    repo.branches.insert(Branch(*splittedline))
    pass

def add_supplier(splittedline : list[str]):
    #TODO: insert the supplier into the repo
    repo.suppliers.insert(Supplier(*splittedline))
    pass

def add_product(splittedline : list[str]):
    #TODO: insert product
    repo.products.insert(Product(*splittedline))
    pass

def add_employee(splittedline : list[str]):
    #TODO: insert employee
    repo.employees.insert(Employee(*splittedline))
    pass

adders = {  "B": add_branch,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    inputfilename = args[1]
    # delete the database file if it exists
    if os.path.isfile("bgumart.db"):
        repo._close()
        os.remove("bgumart.db")


    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            adders.get(splittedline[0])(splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)