from hwiddb import Database
from webserver import web_server

def database_console():
    new_db = Database()
    
    while True:
        userinput = input(
"""
1. Print a table
2. Approve a request
3. Delete a request
4. Update a users date_end
5. Delete a user
6. Exit
""")
        if userinput == '1':
            userinput = input('Enter a table to print: ')
            if userinput == "USER":
                new_db.print_table()
            elif userinput == "REQUESTS":
                new_db.print_table("REQUESTS")
        elif userinput == '2':
            userinput = input('Enter request ID to approve: ')
            new_db.approve_access(userinput)
        elif userinput == '3':
            userinput = input('Enter request ID to delete: ')
            new_db.delete_row(userinput, "REQUESTS")
        elif userinput == '4':
            name = input('Enter name to update: ')
            date = input('Enter new date (YYYY-MM-DD)')
            new_db.set_subscription_end_date(name, date)
        elif userinput == '5':
            userinput = input('Enter ID to delete: ')
            new_db.delete_row(userinput, "USER")
        elif userinput == '6':
            break
    new_db.close()

def main():
    web_server()
    database_console()

if __name__ == '__main__':
    main()
