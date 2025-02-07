from persistence import *

import sys

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            product_id : int = int(splittedline[0])
            quantity : int = int(splittedline[1])
            activator_id : int = int(splittedline[2])
            date : str = splittedline[3]
            product = repo.products.find(id = product_id).fetchone()[0]
            #if sale - check if there is enough enough quantity
            if(quantity < 0 and product.quantity < abs(quantity)):
                #not enough quantity - do nothing
                continue
            else:
                repo.activities.insert(Activitie(product_id, quantity, activator_id, date))
                repo.products.update({"quantity" : (product.quantity + quantity)}, id = product_id)

            

            



if __name__ == '__main__':
    main(sys.argv)