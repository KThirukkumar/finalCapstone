import math

# Present the user with the bond/investment choice menu

menu_choice = input("Choose either 'investment' or 'bond' from the menu below to proceed:\n\ninvestment  -  to calculate the amount of interest you'll earn on your investment\nbond        -  to calculate the amount you'll have to pay on a home loan\n").lower()

# If the user chooses investment
if menu_choice == "investment":
    deposit = float(input("Please enter the amount of money you are depositing: "))
    interest_rate = float(input("Please enter the interest rate: "))
    term_length = float(input("Please enter the number of years you plan on investing: "))
    interest = input("Would you like simple or compound interest? ")
    if interest.lower() == "simple":
        total = deposit * (1 + (interest_rate / 100) * term_length)
    else:
        total = deposit * math.pow((1 + (interest_rate / 100)), term_length)

    print(f"The total equals {round(total,2)}.")

# If the user chooses bond
else:
    present_value = float(input("Please enter the present value of the house: "))
    interest_rate = float(input("Please enter the interest rate: "))
    term_length = float(input("Please enter the number of months you plan to repay the bond over: "))
    repayment = (((interest_rate/ 100) / 12) * present_value) / (1 - math.pow((1 + ((interest_rate / 100) / 12)), (-1 * term_length)))
    print(f"You will have to pay back {round(repayment,2)} every month.")