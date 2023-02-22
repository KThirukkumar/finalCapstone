#========Imported Libraries==========
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = float(quantity)

    def get_cost(self):
        return float(self.cost)

    def get_quantity(self):
        return float(self.quantity)

    def __str__(self):
        return f"{self.product}"

#=============Shoe list===========
shoe_list = []

#==========Functions outside the class==============
def read_shoes_data():
    with open('inventory.txt', 'r') as f:
        f = f.read().split('\n')
        for line in range(1, len(f)):
            try:
                line = f[line].split(",")
                shoe_list.append(Shoe(line[0], line[1], line[2], line[3], line[4]))
            except Exception:
                print("There has been an error. Please check inventory.txt.")
    print("Upload complete.")

def capture_shoes():
    country = input("Please enter the country: ")
    code = input("Please enter the code of the shoe: ")
    product = input("Please enter the shoe product name: ")
    cost = input("Please enter the cost of the shoe: ")
    quantity = input("Please enter the quantity of the shoe: ")
    shoe_list.append(Shoe(country, code, product, cost, quantity))

def view_all():
    shoes_list = [["Country", "Code", "Product", "Cost", "Quantity"]]
    for shoe in shoe_list:
        shoes_list.append([shoe.country,shoe.code, shoe.product, shoe.cost, shoe.quantity])
    print(f"\nHere are all the stored shoes:\n{tabulate(shoes_list)}")

def re_stock():
    shoe_amount = 0
    shoe_name = ""
    shoe_index = 0
    for count, shoe in enumerate(shoe_list):
        # Assigns first item in list to be lowest quantity
        if shoe_list.index(shoe) == 0:
            shoe_amount = shoe.get_quantity()
            shoe_name = shoe.product

        # Compare shoe quantities to first shoe
        if shoe.get_quantity() < shoe_amount:
            shoe_amount = shoe.get_quantity()
            shoe_name = shoe.product
            shoe_index = count

    # Ensure user enters an integer
    restock_number = ""
    while not isinstance(restock_number, int):
        try:
            restock_number = int(input(f"How many {shoe_name} shoes would you like to add to the stocks? "))
        except Exception:
            print("You have entered an invalid number. Please try again")
    
    # Add quantity to shoe stock
    shoe_list[shoe_index].quantity = shoe_list[shoe_index].quantity + restock_number
    print(f"There are now {shoe_list[shoe_index].quantity} {shoe_name} shoes.")

def seach_shoe(shoe_code):
    shoe = [shoe for shoe in shoe_list if shoe.code == shoe_code]
    return shoe[0]

def value_per_item():
    shoes = [["Product", "Value"]]
    for shoe in shoe_list:
        shoes.append([shoe.product, (shoe.get_quantity() * shoe.get_cost())])
    print(tabulate(shoes))

def highest_qty():
    shoe_amount = 0
    shoe_name = ""
    for shoe in shoe_list:
        if shoe.get_quantity() > shoe_amount:
            shoe_amount = shoe.get_quantity()
            shoe_name = shoe.product

    print(f"{shoe_name} is on sale!")

#==========Main Menu=============
user_choice = ""

while user_choice != "8":
    user_choice = input("""\nWelcome to the Shoe Inventory Management Program!
Available options:
1) Read Shoes Data
2) Capture Shoes
3) View All Shoes
4) Restock Shoes
5) Search Shoes
6) Value Per Item
7) Find Highest Quantity
8) Quit
Which numbered option would you like to pick? """)

    if user_choice == "1":
        read_shoes_data()
    
    elif user_choice == "2":
        capture_shoes()
    
    elif user_choice == "3":
        view_all()
    
    elif user_choice == "4":
        re_stock()
    
    elif user_choice == "5":
        search_code = input("Please enter the code you would like search with: ")
        try:
            print(f"The code {search_code} corresponds to {seach_shoe(search_code)}.")
        except Exception:
            print("The code has not been found within our inventory.")

    
    elif user_choice == "6":
        value_per_item()
    
    elif user_choice == "7":
        highest_qty()
    
    elif user_choice == "8":
        print("Thank you for using the Shoe Inventory Management Program. Goodbye!")
    
    else:
        print("Invalid option has been entered. Please try again.")