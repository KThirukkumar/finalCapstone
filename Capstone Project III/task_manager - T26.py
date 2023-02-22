#=====importing libraries===========
'''This is the section where you will import libraries'''
import datetime

#=====functions===========

# Optional function added to increase modularity  
def header_printer(header):
    print(f"_________________________________\n\nWelcome to {header}\n_________________________________\n")

def reg_user():
    # User Registration Header
    header_printer("User Registration")

    # Gets Registration Details from User
    new_username = input("Please enter a username for the new user: ")
    
    # Checks if username already exists  in user.txt
    with open('user.txt') as f:
        for line in f:
            if new_username == line[:line.index(",")]:
                while new_username == line[:line.index(",")]:
                    print(f"Error: The username [{new_username} already exists. Please enter a new username.")
                    new_username = input("\nPlease enter a new username for the new user: ")
    
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

def add_task():
    # Task Administration Header
    header_printer("Task Administration")

    # Enter task details
    assigned_username = input("Please enter username the task is assigned to: ")
    task_title = input("Enter the task's title: ")
    task_description = input("Please enter a description of the task: ")
    due_date = input("Please enter the due date of the task in the format (Day Month Year): ")

    # Get current date
    current_date = str(datetime.date.today())

    # Append task details to tasks.txt
    with open('tasks.txt', 'a+') as f:
        f.write('\n' + ', '.join([assigned_username, task_title, task_description, current_date, due_date, "No"]))
    
    # Return back to Main Menu
    print("\n_________________________________\n\nExiting Task Administration. Returning back to Main Menu. \n_________________________________\n")

def view_all():
    # All Tasks Header
    header_printer("All Tasks")

    # Read tasks.txt
    with open('tasks.txt', 'r') as f:
        f = f.read().split("\n")

        # Iterate through each task
        for task in f:
            if task != "":
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

def view_mine(username):
    # User Tasks Header
    header_printer(f"Tasks for {username}")
    # Read tasks.txt
    tasks = []
    with open('tasks.txt', 'r') as f:
        task_list = f.read().split("\n")
        # Iterate through tasks
        count = 0
        # User-specific tasks are kept track in the format:
        # count : task_list index
        task_dict = {}

        for task in task_list:
            assigned_user = task.split(", ")[0]
            # Continue loop if task is not assigned to user
            if assigned_user != username:
                continue
            tasks.append(task)
            task_dict[str(count)] = task_list.index(task)
            task_title = task.split(", ")[1]
            task_description = task.split(", ")[2]
            assigned_date = task.split(", ")[3]
            due_date = task.split(", ")[4]
            task_complete = task.split(", ")[5]
            count += 1
            
            # Present Task details separated by a line
            print(f"{f'Task {count}:': <20} {task_title}" +
            f"\n{'Date assigned:': <20} {assigned_date}" +
            f"\n{'Due date:': <20} {due_date}" +
            f"\n{'Task Complete?': <20} {task_complete}" +
            f"\n{'Task description:': <20} {task_description}" +
            "\n___________________________\n")
        
        # Task Editing
        task_editing = int(input("Please select a task number to edit or enter -1 to return to the main menu: "))
        
        if int(task_editing) > 0 and int(task_editing) <= len(tasks):
            task_edit = input("Would you like to edit the task or mark the task as complete? Please enter 'edit' or 'complete': ")
            
            task_to_be_edited = task_list[task_editing-1].split(", ")

            # Edit Task
            if task_edit.lower() == "edit":
                if task_to_be_edited[5] == "No":
                    editing_choice = input("Would you like to edit username of the person to whom the task is assigned to or the due date of the task? Please enter 'username' or 'date': ")
                    
                    # Assign new username to task
                    if editing_choice.lower() == "username":
                        new_username = input("Please enter new username: ")
                        task_to_be_edited[0] = new_username
                        print(f"Success: {new_username} has been assigned to task {task_editing}.")
                    
                    # Assign new date to task
                    elif editing_choice.lower() == "date":
                        new_date = input("Please enter the due date of the task in the format (YYYY-MM-DD): ")
                        task_to_be_edited[4] = new_date
                        print(f"Success: {new_date} has been assigned to task {task_editing}.")

                else:
                    print("Task has been completed and cannot be edited.")
            
            # Mark task as complete
            elif task_edit.lower() == "complete":
                task_to_be_edited[5] = "Yes"
                print(f"Success: Task {task_editing} has been marked complete.")

            # Invalid Option entered
            else:
                print("Error: Invalid option entered.")

            # Rejoin and replace task within tasks list
            tasks[task_editing-1] = ", ".join(task_to_be_edited)
            task_list[task_dict[str(task_editing-1)]] = tasks[task_editing-1]
    
    with open('tasks.txt', 'w') as f:
        # Write Edited Tasks to file            
        for task in task_list:
            f.write(task + '\n')


    print(f"_________________________________\n\nExiting Tasks for {username}. Returning to Main Menu.\n_________________________________\n")

def generate_report():
    # Assigns returned values to eponymous variables
    total_tasks, total_users, completed_tasks, overdue_tasks, uncompleted_tasks, user_overview = tasks_calculation()

    # Calls task_overview_display function to output data to task_overview.txt
    task_overview_display(total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks)

    # Calls user_overview_display function to output data to user_overview.txt
    user_overview_display(total_tasks, total_users, user_overview)

# Responsible for Task Calculation
def tasks_calculation():
    total_tasks = 0
    completed_tasks = 0
    overdue_tasks = 0
    user_overview = {}

    with open('user.txt', 'r') as f:
        total_users = len(f.read().split("\n"))

    with open('tasks.txt', "r") as t:
        t = t.read().split("\n")

        # Iterate through each task
        for task in t:
            if task != "":
                total_tasks += 1
                # Add Username to User Overview Dictionary
                if task.split(", ")[0] not in list(user_overview):
                    user_overview[task.split(", ")[0]] = {}

                # Check if task is complete
                if task.split(", ")[5] == "Yes":
                    completed_tasks += 1
                
                # Check if task is overdue
                if task.split(", ")[5] == "No" and datetime.datetime.strptime(str(str(task.split(", ")[4].split(" ")[2]) + "-" + str(datetime.datetime.strptime(task.split(", ")[4].split(" ")[1],'%b').month) + "-" + str(task.split(", ")[4].split(" ")[0])), "%Y-%m-%d").date() > datetime.date.today() > str(datetime.date.today()):
                    overdue_tasks += 1

        # Calculate total incomplete tasks   
        uncompleted_tasks = total_tasks - completed_tasks

        # Create a nested dictionary made up of Users as keys
        for user in list(user_overview):
            user_total_tasks = 0
            user_completed_tasks = 0
            user_uncompleted_tasks = 0
            user_overdue_tasks = 0

            # Iterate through task
            for task in t:
                if task.split(", ")[0] == user:
                    user_total_tasks += 1

                    # Check if task is complete
                    if task.split(", ")[5] == "Yes":
                        user_completed_tasks += 1
                    
                    # Check if task is overdue
                    if task.split(", ")[5] == "No" and datetime.datetime.strptime(str(str(task.split(", ")[4].split(" ")[2]) + "-" + str(datetime.datetime.strptime(task.split(", ")[4].split(" ")[1],'%b').month) + "-" + str(task.split(", ")[4].split(" ")[0])), "%Y-%m-%d").date() > datetime.date.today() > str(datetime.date.today()):
                        user_overdue_tasks += 1
                        
            # Calculate total incomplete tasks 
            user_uncompleted_tasks = user_total_tasks - user_completed_tasks
            
            # Add each required value to the user_overview nested dictionary
            user_overview[user]["Total Tasks"] = user_total_tasks
            user_overview[user]["Total Tasks Percentage"] = user_total_tasks / total_tasks * 100
            user_overview[user]["Completed Tasks"] = user_completed_tasks / user_total_tasks * 100
            user_overview[user]["Uncompleted Tasks"] = user_uncompleted_tasks / user_total_tasks * 100
            user_overview[user]["Overdue Tasks"] = user_overdue_tasks / user_total_tasks * 100

    return total_tasks, total_users, completed_tasks, overdue_tasks, uncompleted_tasks, user_overview

# Responsible for outputting data to task_overview.txt
def task_overview_display(total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks):
    with open('task_overview.txt', 'w') as f:
        f.write(f"""------------------------ Welcome to Task Overview -----------------------
{"Total Tasks:" : <40} {str(total_tasks)}
{"Completed Tasks:" : <40} {str(completed_tasks)}
{"Uncompleted Tasks:" : <40} {str(uncompleted_tasks)}
{"Overdue Tasks:" : <40} {str(overdue_tasks)}
{"Percentage of Tasks that are incomplete:" : <40} {str((uncompleted_tasks / total_tasks * 100)) + " %"}
{"Percentage of Tasks that are overdue:" : <40} {str((overdue_tasks / total_tasks * 100)) + " %"}
\n-------------------------------------------------------------------------""")

# Responsible for outputting data to user_overview.txt
def user_overview_display(total_tasks, total_users, user_overview):
    with open('user_overview.txt', 'w') as f:
        f.write(f"""\n----------------------- Welcome to User Overview ------------------------\n
{"Total Users Registered:" : <65} {str(total_users)}
{"Total Tasks Registered:" : <65} {str(total_tasks)}""")
        for user in list(user_overview):
            f.write(f"""\n\n------------------------ {user}'s Task Overview ------------------------\n
{"Total Number of Tasks Assigned to User:" : <65} {str(user_overview[user]["Total Tasks"])}
{"Percentage of Total Tasks Assigned to User:" : <65} {str(user_overview[user]["Total Tasks Percentage"]) + " %"}
{"Percentage of Tasks Assigned to User that have been Completed:" : <65} {str(user_overview[user]["Completed Tasks"]) + " %"}
{"Percentage of Tasks Assigned to User that are Incomplete:" : <65} {str(user_overview[user]["Uncompleted Tasks"]) + " %"}
{"Percentage of Tasks Assigned to User that are Overdue:" : <65} {str(user_overview[user]["Overdue Tasks"]) + " %"}
\n-------------------------------------------------------------------------""")

# Display Statistics
def display_statistics():
    # Updates reports by generating new reports
    generate_report()

    # Displays task_overview.txt on terminal
    with open('task_overview.txt', 'r') as f:
        print("\n" + f.read())

    # Displays user_overview.txt on terminal
    with open('user_overview.txt', 'r') as f:
        print("\n" + f.read())
    
    

    print(f"\n_________________________________\n\nExiting Statistics. Returning to Main Menu.\n_________________________________\n")

#====Login Section====
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
gr - Generate Reports
ds - Display Statistics
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
        reg_user()

    # Task Administration
    elif menu == 'a':
        add_task()

    # View All Tasks    
    elif menu == 'va':
        view_all()

    # View User's Tasks
    elif menu == 'vm':
        view_mine(username)

    # Admin Menu
    elif menu == 'ds' and username == 'admin':
        display_statistics()

    elif menu == 'gr' and username == 'admin':
        generate_report()

    # Exit
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please try again.")