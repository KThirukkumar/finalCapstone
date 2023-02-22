#=====importing libraries===========
'''This is the section where you will import libraries'''
import datetime

#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''
login = False

while login == False:
    # Load user.txt details and store details in a dictionary
    user_details = {}
    with open('user.txt', 'r') as f:
        f = f.read().split('\n')
        for line in f:
            # Remove comma and whitespace
            # Add username as key and password as value to dictionary
            user_details[line.split(', ')[0]] = line.split(', ')[1]

    print("_________________________________\n\nLogin Menu:\n_________________________________\n")
    
    # Request login information from user
    username = input("Please enter your username: ")
    password = input("Please enter your account password: ")
    
    # Checks entered login details with stored details
    if username in list(user_details.keys()):
        if password == user_details[username]:
            # User greeting
            print(f"""\n_________________________________\n\n       Login Successful\n\nWelcome {username},\n""")
            login = True
            
        # Message to user in the case of an incorrect password
        else:
            print("\nInvalid password. Please check your password and try again.")
    # Message to user in the case of an incorrect username
    else:
        print("\nInvalid login details. Please check your username and try again.")
    

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    # Presents special menu to admin
    print("_________________________________\n\nWelcome to the Main Menu\n_________________________________\n")
    if username == 'admin':
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
s - Admin Menu
e - Exit
: ''').lower()
    
    # Presents non-admin menu
    else:
        menu = input('''Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    # Registration Menu - Only available to Admin
    if menu == 'r' and username == 'admin':
        # User Registration Header
        print("_________________________________\n\nWelcome to User Registration\n_________________________________\n")
        
        # Gets Registration Details from User
        new_username = input("Please enter a username for the new user: ")
        new_password = input("Please enter a new password: ")
        confirm_password = input("Please re-enter the password for confirmation: ")

        # Writes New User Details to user.txt
        if new_password == confirm_password:
            with open('user.txt', 'a') as f:
                f.write('\n' + ', '.join([new_username,new_password]))

        # Presents message if passwords do not match
        else: print("\nError: Passwords do not match.\n")
        
        # Return back to Main Menu
        print(f"\n_________________________________\n\nRegistration Successful. You have successfully registered: \n\nUser: {new_username}\n\nExiting User Registration. Returning to the Main Menu.\n_________________________________\n")

    # Task Administration
    elif menu == 'a':
        # Task Administration Header
        print("_________________________________\nWelcome to Task Administration\n_________________________________\n")
        
        # Enter task details
        assigned_username = input("Please enter username the task is assigned to: ")
        task_title = input("Enter the task's title: ")
        task_description = input("Please enter a description of the task: ")
        due_date = input("Please enter the due date of the task in the format (YYYY-MM-DD): ")

        # Get current date
        current_date = str(datetime.date.today())

        # Append task details to tasks.txt
        with open('tasks.txt', 'a+') as f:
            f.write('\n' + ', '.join([assigned_username, task_title, task_description, current_date, due_date, "No"]))
        
        # Return back to Main Menu
        print("\n_________________________________\n\nExiting Task Administration. Returning back to Main Menu. \n_________________________________\n")

    # View All Tasks    
    elif menu == 'va':
        # All Tasks Header
        print("\n_________________________________\nAll Tasks\n_________________________________\n")
        
        # Read tasks.txt
        with open('tasks.txt', 'r') as f:
            f = f.read().split("\n")

            # Iterate through each task
            for task in f:
                assigned_user = task.split(", ")[0]
                task_title = task.split(", ")[1]
                task_description = task.split(", ")[2]
                assigned_date = task.split(", ")[3]
                due_date = task.split(", ")[4]
                task_complete = task.split(", ")[5]

                # Present Task details separated by a line
                print(f"{'Task:': <20} {task_title}" +
                f"\n{'Assigned to:': <20} {assigned_user}" +
                f"\n{'Date assigned:': <20} {assigned_date}" +
                f"\n{'Due date:': <20} {due_date}" +
                f"\n{'Task Complete?': <20} {task_complete}" +
                f"\n{'Task description:': <20} {task_description}" +
                "\n___________________________\n")
        print("_________________________________\n\nExiting All Tasks. Returning to Main Menu.\n_________________________________\n")

    # View User's Tasks
    elif menu == 'vm':
        # User Tasks Header
        print(f"\n_________________________________\nTasks for {username}\n_________________________________\n")
        
        # Read tasks.txt
        with open('tasks.txt', 'r') as f:
            f = f.read().split("\n")
            # Iterate through tasks
            for task in f:
                assigned_user = task.split(", ")[0]
                # Continue loop if task is not assigned to user
                if assigned_user != username:
                    continue
                task_title = task.split(", ")[1]
                task_description = task.split(", ")[2]
                assigned_date = task.split(", ")[3]
                due_date = task.split(", ")[4]
                task_complete = task.split(", ")[5]
                
                # Present Task details separated by a line
                print(f"{'Task:': <20} {task_title}" +
                f"\n{'Date assigned:': <20} {assigned_date}" +
                f"\n{'Due date:': <20} {due_date}" +
                f"\n{'Task Complete?': <20} {task_complete}" +
                f"\n{'Task description:': <20} {task_description}" +
                "\n___________________________\n")
        print(f"_________________________________\n\nExiting Tasks for {username}. Returning to Main Menu.\n_________________________________\n")
    
    # Admin Menu
    elif menu == 's' and username == 'admin':
        # Admin Menu Header
        print("_________________________________\n\nWelcome to Admin Menu\n_________________________________\n")
        number_of_tasks = 0
        number_of_users = 0
        # Reads user.txt and counts number of users
        with open('user.txt', 'r') as f:
            f = f.read().split("\n")
            for count in range(len(f)):
                number_of_users += 1

        # Reads tasks.txt and counts number of tasks
        with open('tasks.txt', 'r') as f:
            f = f.read().split("\n")
            for count in range(len(f)):
                number_of_tasks += 1

        # Present "Number of Users" and "Number of Tasks"
        print(f"{'Number of Users:' : <5} {number_of_users}\n{'Number of Tasks:' : <5} {number_of_tasks}")

        print(f"\n_________________________________\n\nExiting Admin Menu. Returning to Main Menu.\n_________________________________\n")

    # Exit
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")