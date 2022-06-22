#!/usr/bin/env python3

import sys, os, pickle, datetime
import account_functions
import user_functions

class Account:
    def __init__(self, name, initial_deposit = 0):
        self.account_log = dict()
        self.name = name
        self.value = initial_deposit
        self.password = "unset"
    def get_value(self):
        return self.value
    def make_deposit(self, amount):
        self.value += amount
        self.update_account_log(action="Deposit", amount=amount)
    def make_withdrawal(self, amount):
        self.value -= amount
        self.update_account_log(action="Withdrawal", amount=amount)
    def get_password(self):
        return self.password
    def set_password(self, new_password):
        self.password = new_password
    def update_account_log(self, action, amount):
        date = datetime.datetime.now()
        self.account_log[date] = [action, amount]
    def get_account_log(self):
        return self.account_log
    def view_account_log(self):
        for date in self.account_log.keys():
            print(f'{date}: action: {self.account_log[date][0]} amount: {self.account_log[date][1]}')
    def __str__(self):
        return f'\n\n***************\nAccount Name: {self.name}\nAccount Value: {self.value}\n***************\n'

class User:
    def __init__(self, name):
        self.name = name
        self.user_accounts = []
        self.password = 'unset'
    def add_account(self, account_name):
        if account_name not in accounts_dict.keys():
            print("no account named {}".format(account_name))
        else:
            self.user_accounts.append(account_name)
    def remove_account(self, account_name):
        if account_name not in self.user_accounts:
            print(f'{account_name} not in {self.name} accounts')
    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password
    def get_user_accounts(self):
        return self.user_accounts
    def get_user_name(self):
        return self.name
    def set_user_name(self, name):
        self.name = name
    def view_user_accounts(self):
        accounts_string = "\n***** Accounts for {} *****".format(self.name)
        for account in self.user_accounts:
            accounts_string += "\n {}".format(account)
        accounts_string += "\n"
        print(accounts_string)


accounts_dict = dict()
users_dict = dict()

option_dict = {
    "a": "access account",
    "c":"create an account",
    "n": "create new user",
    "u": "login as user",
    "v": "view public accounts",
    "vu": "view user accounts",
    "q": "quit"
}

account_options = {
    "d": "make a deposit",
    "w": "make a withdrawal",
    "l": "view account log",
    "p": "set a password",
    "e": "export log as csv file",
    "del": "delete account",
    "r": "return to start menu"     
}

user_options = {
    "add": "add an account to this user",
    "acc": "access an account beloning to user",
    "p": "set a password for this user",
    "n": "rename user",
    "v": "view user accounts",
    "r": "return to start menu"
}

def save_accounts():
    with open ('accounts.pickle', 'wb') as f:
        pickle.dump(accounts_dict, f)

def save_users():
    with open('users.pickle', 'wb') as f:
        pickle.dump(users_dict, f)

def create_account():
    account_name = input("Name Account: ")
    if account_name not in accounts_dict.keys():
        initial_deposit = input("Initial Deposit: ")
        account = Account(account_name, int(initial_deposit))
        accounts_dict[account_name] = account
        save_accounts()
        account_accessed(account_name)
    else:
        print("Account name taken, please use a new name.")
        create_account()

def process_account_choice(account_name, option):
    if option == "d":
        account_functions.deposit(accounts_dict, account_name)
    elif option == "w":
        account_functions.withdrawal(accounts_dict, account_name)
    elif option == "l":
        accounts_dict[account_name].view_account_log()
    elif option == "p":
        account_functions.set_password(accounts_dict, account_name)
    elif option == "e":
        account_functions.export_logs_as_csv(accounts_dict, account_name)
    elif option == "r":
        start_menu()
    elif option == "del":
        account_functions.delete_account(accounts_dict, account_name)
        save_accounts()
        start_menu()
    save_accounts()
    account_accessed(account_name)

def account_accessed(account_name):
    print("Access Acount {}".format(accounts_dict[account_name]))
    for option in account_options.keys():
        print(f'To {account_options[option]} press {option}')
    user_choice = input("Select option: ")
    while user_choice not in account_options.keys():
        print(f'\n{user_choice} is not an available option.')
        user_choice = input("Please select a choice from the menu: ")
    print(f'\nYou choose to {account_options[user_choice]}')
    process_account_choice(account_name, user_choice)
    start_menu()

def access_account():
    account_name = input("Enter Account Name: ")
    if account_name in accounts_dict.keys():
        print(f'password: {accounts_dict[account_name].get_password()}')
        if accounts_dict[account_name].get_password() == 'unset':
            account_accessed(account_name)
        else:
            ps_word_attempt = input("Please enter password: ")
            if ps_word_attempt == accounts_dict[account_name].get_password():
                account_accessed(account_name)
            else:
                print("Sorry, incorrect password")
                start_menu()
    else:
        print("No account named: {}".format(account_name))
        start_menu()

def view_accounts():
    print("\nAccounts Available")
    for key in accounts_dict.keys():
        print(key)
    start_menu()

def process_user_choice(choice, user_name):
    if choice == "add":
        user_functions.add_account(user_name=user_name, users_dict=users_dict, accounts_dict=accounts_dict)
        save_accounts()
    elif choice == "acc":
        if len(users_dict[user_name].get_user_accounts()) > 0:
            for account in users_dict[user_name].get_user_accounts():
                print('\n {}'.format(account))
            selection = input("Account Selection: ")
            while selection not in users_dict[user_name].get_user_accounts():
                input("Please select an account associated with user: ")
            account_accessed(selection)
        else:
            print("No accounts associated with this user yet!")
    elif choice =="p":
        if users_dict[user_name].get_password() == 'unset' or users_dict[user_name].get_password() == input("Enter password: "):
            ps_word = input("Enter Password for {}".format(user_name))
            users_dict[user_name].set_password(ps_word)
        else:
            print("Sorry wrong password")
    elif choice == "n":
        if users_dict[user_name].get_password() == 'unset' or users_dict[user_name].get_password() == input("Enter password: "):
            new_name = input("Enter new name: ")
            user = users_dict.pop(user_name)
            user.set_user_name(new_name)
            users_dict[new_name] = user
            save_users()
    elif choice == "v":
        users_dict[user_name].view_user_accounts()
    elif choice == "r":
        start_menu()
    user_accessed(user_name)

def user_accessed(name):
    print(f'Accesed User {name}')
    for key in user_options.keys():
        print(f'To {user_options[key]} input {key}')
    user_choice = input("Select a choice: ")
    while user_choice not in user_options.keys():
        user_choice = input("Please select an option from the menu: ")
    print(f'\nYou chose to {user_options[user_choice]}')
    process_user_choice(user_choice, name)

def access_user():
    user_name = input("Enter user name: ")
    if user_name in users_dict.keys():
        if users_dict[user_name].get_password() == 'unset':
            user_accessed(user_name)
        else:
            ps_word_attempt = input("Please enter user password: ")
            if users_dict[user_name].get_password() == ps_word_attempt:
                user_accessed(user_name)
            else:
                print("Sorry wrong password for {}".format(user_name))
                start_menu()
    else:
        print(f'no user named {user_name}')
        start_menu()

def create_user():
    name = input("New user name: ")
    while name in users_dict.keys():
        name = input("Please choose a name that isn't taken: ")
    user = User(name)
    users_dict[name] = user
    save_users()
    user_accessed(name)

def view_users():
    print("\n***** Users *****")
    for key in users_dict.keys():
        print(key)
    start_menu()

def quit():
    sys.exit()

def process_choice(choice):
    if choice == "c":
        create_account()
    elif choice == "a":
     access_account()
    elif choice == "v":
        view_accounts()
    elif choice == "q":
        quit()
    elif choice == "n":
        create_user()
    elif choice == "u":
        access_user()
    elif choice == "vu":
        view_users()
    else:
        print("please select an option from the menu")
        choice = input("Choice: ")
        process_choice(choice)

def start_menu():
    welcome_string =  "\n**************\nWelcome to Account Manager!\n**************"
    for option in option_dict.keys():
        welcome_string += "\nTo {} press {}".format(option_dict[option], option)
    print(welcome_string)
    choice = input("\nChoice: ")
    process_choice(choice)

def load_accounts():
    global accounts_dict
    if os.path.isfile('accounts.pickle'):
        with open('accounts.pickle', 'rb') as f:
            accounts_dict = pickle.load(f)
            # print("loading accounts: "+ str(accounts_dict))

def load_users():
    global users_dict
    if os.path.isfile('users.pickle'):
        with open('users.pickle', 'rb') as f:
            users_dict = pickle.load(f) 
            # print("loading users: "+ str(users_dict))

def main(args):
    load_accounts()
    load_users()
    if len(args) > 1 and args[1] in option_dict.keys():
        process_choice(args[1])
    else:
        start_menu()

if __name__ == '__main__':
    main(sys.argv)