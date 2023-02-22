#=====importing libraries===========
import sqlite3

#=====database===========
db = sqlite3.connect('data/ebookstore_db')

cursor = db.cursor()

cursor.execute('''
    SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books'
''')

# Check if table already exists
if cursor.fetchone()[0]==0:
    # Create table
    cursor.execute('''
        CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
    ''')

    db.commit()

    books = [
        (3001,'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002,'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
        (3003,'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
        (3004,'The Lord of the Rings', 'J.R.R. Tolkein', 37),
        (3005,'Alice in Wonderland', 'Lewis Carroll', 12),
    ]

    # Populate table with books
    cursor.executemany('''
        INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)
    ''', books)
    db.commit()

#=====menu functions===========

# Optional function added to increase modularity  
def header_printer(header):
    print(f"_________________________________\n\nWelcome to {header}\n_________________________________\n")

# Enter book function
def enter_book():
    # User Registration Header
    header_printer("Book Registration")

    # Get book details from user
    title = input("Please enter the book's title: ")
    author = input("Please enter the book's author: ")
    id = None
    qty = None

    # Ensure ID is an integer through while loop
    while not isinstance(id, int):
        try:
            id = int(input(f"Please enter an ID for {title}: "))
        except:
            print(f"Error: ID must be an integer.\n")
    
    # Ensure Quantity is an integer through while loop
    while not isinstance(qty, int):
        try:
            qty = int(input(f"Please enter the quantity of {title}: "))
        except:
            print(f"Error: Quantity must be an integer.\n")
    
    # Add book to table
    cursor.execute('''
        INSERT INTO books(id, Title, Author, Qty) 
        VALUES(?,?,?,?)''', (id, title, author, qty))

    # Commit database
    db.commit()

    # Return back to Main Menu
    print(f"\n_________________________________\n\nAddition Successful. You have successfully added: \n\nTitle: {title}\n\nExiting Book Registration. Returning to the Main Menu.\n_________________________________\n")

# Update book Function
def update_book():
    # Task Administration Header
    header_printer("Book Updates")

    # Collect all IDs of books
    ids = []

    # Display inventory to assist user
    cursor.execute('''
    SELECT * FROM books
    ''')
    print(f"|{'ID':<6} | {'Title':<50} | {'Author':<50} | {'Qty':<6} | ")
    for row in cursor:
        print(f"|{row[0]:<6} | {row[1]:<50} | {row[2]:<50} | {row[3]:<6} | ")
        # Add book id to ids 
        ids.append(row[0])
    
    # Cast ids' contents into strings
    ids = [str(id) for id in ids]

    # Ensure entered ID is an integer
    selection = None
    while not isinstance(selection,int):
        try:
            selection = int(input("\nPlease enter the ID of the book you would like to update: "))
        except:
            print("Error: ID must be an integer.\n")
    
    # Select Column Value to edit for the book
    column = ""
    while column.lower() not in ["id", "title", "author", "quantity"]:
        column = input("Would you like to change the ID, Title, Author's name, or the Quantity? Please enter 'ID', 'Title', 'Author' or 'Quantity': ")
    # Cast entered ID into a string
    selection = str(selection)

    # Check to see entered ID is in the inventory
    if selection in ids:
        # Change ID
        if column.lower() == "id":
            id = None
            while not isinstance(id, int):
                try:
                    id = int(input(f"Please enter an ID for the book with ID: {selection}: "))
                except:
                    print(f"Error: IDs must be an integer.")

            cursor.execute('''
                UPDATE books SET id = ? WHERE id = ?
            ''', (id, selection))

        # Change Title
        elif column.lower() == "title":
            title = input("Please enter the new title: ")
            cursor.execute('''
                UPDATE books SET Title = ? WHERE id = ?
            ''', (title, selection))

        # Change Author
        elif column.lower() == "author":
            author = input("Please enter the book's author's updated name: ")
            cursor.execute('''
                UPDATE books SET author = ? WHERE id = ?
            ''', (author, selection))

        # Change Quantity
        elif column.lower() == "quantity":
            qty = None
            while not isinstance(qty, int):
                try:
                    qty = int(input(f"Please enter the quantity for the book with ID:{selection}: "))
                except:
                    print(f"Error: Quantities need to be an integer")

            cursor.execute('''
                UPDATE books SET Qty = ? WHERE Title = ?
            ''', (qty, selection))
    
    # Inform the user-entered ID is not in the inventory
    else:
        print(f"{selection} is not within the inventory.")

    db.commit()
    
    # Return back to Main Menu
    print("\n_________________________________\n\nExiting Book Updates. Returning back to Main Menu. \n_________________________________\n")

# Delete Book Function
def delete_book():
    # Book Deletion Header
    header_printer("Book Deletion")

    # Collect all IDs of books
    ids = []

    # Display inventory to assist user
    cursor.execute('''
    SELECT * FROM books
    ''')
    print(f"|{'ID':<6} | {'Title':<50} | {'Author':<50} | {'Qty':<6} | ")
    for row in cursor:
        print(f"|{row[0]:<6} | {row[1]:<50} | {row[2]:<50} | {row[3]:<6} | ")
        # Append ID into ids list
        ids.append(row[0])

    # Cast ids' contents into strings
    ids = [str(id) for id in ids]
    
    # Ensure entered ID is an integer
    selection = None
    while not isinstance(selection,int):
        try:
            selection = int(input("\nPlease enter the ID of the book you would like to remove: "))
        except:
            print("Error: ID must be an integer.\n")

    # Delete the book if user-entered ID corresponds to a book in the inventory
    if str(selection) in ids:
        cursor.execute('''DELETE FROM books WHERE id=?''', (str(selection),))
        print(f"\nID Number {selection} has been deleted from the inventory.")

    # Inform the user that the book ID doesn't correspond to a book in the inventory
    else:
        print(f"\nID Number {selection} does not exist within the inventory.")
    
    db.commit()

    print("_________________________________\n\nExiting Book Deletion. Returning to Main Menu.\n_________________________________\n")

# Search Books Function
def search_books():
    # Book Search Header
    header_printer("Book Search")

    # Get title of book from user
    selection = input("Please enter the title of the book you would like to find: ")

    # Parse through table while collecting all rows with user-entered title
    cursor.execute('''
            SELECT * FROM books WHERE title = ?
            ''', (selection,))
    
    # Collect all titles that are equal to selection
    titles = []
    for row in cursor:
        titles.append(row[1])

    # Display book details if user-entered title exists within the table
    if selection in titles:
        print(f"\n{selection} exists within the inventory. \n|{'ID':<6} | {'Title':<50} | {'Author':<50} | {'Qty':<6} | ")
        print(f"|{row[0]:<6} | {row[1]:<50} | {row[2]:<50} | {row[3]:<6} | ")
    # Inform the user that book doesn't exist within the table.
    else:
        print(f"\n'{selection}' does not exist within the inventory.")

    db.commit()

    print("_________________________________\n\nExiting Book Search. Returning to Main Menu.\n_________________________________\n")

# View Inventory
def view_table():
    # Book Search Header
    header_printer("View Inventory")

    # Parse through all rows in table
    cursor.execute('''
            SELECT * FROM books''')
    # Column Headers
    print(f"\n|{'ID':<6} | {'Title':<50} | {'Author':<50} | {'Qty':<6} | ")
    
    # Display all rows
    for row in cursor:
        print(f"|{row[0]:<6} | {row[1]:<50} | {row[2]:<50} | {row[3]:<6} | ")


    db.commit()

    print("_________________________________\n\nExiting Inventory. Returning to Main Menu.\n_________________________________\n")


#====Login Section====
book_menu = True   
while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    # Presents special menu to admin
    print("_________________________________\n\nWelcome to the Main Menu\n_________________________________\n")
    
    menu = input('''Select one of the following Options below:
a - Add a new book to the database
u - Update book information
d - Delete a book from the database
s - Search the database to find a specific book
v - View inventory
e - Exit
: ''').lower()
    

    # Add a new book to the database
    if menu == 'a':
        enter_book()

    # Update book information
    elif menu == 'u':
        update_book()

    # Delete a book from the database
    elif menu == 'd':
        delete_book()

    # Search the databse to find a specific book
    elif menu == 's':
        search_books()

    elif menu == 'v':
        view_table()
    
    # Exit
    elif menu == 'e':
        print('Goodbye!')
        db.close()
        book_menu = False 

        exit()

    else:
        print("You have made a wrong choice. Please try again.")