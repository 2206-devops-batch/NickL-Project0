

def add_account(user_name, users_dict, accounts_dict):
    account_name = input("Account name: ")
    if account_name in accounts_dict.keys():
        users_dict[user_name].add_account(account_name)
    else:
        print(f'\nno account named {account_name}\n')

def  access(user_name, users_dict):
    if users_dict[user_name].get_user_accounts() > 0:
        for account in users_dict[user_name].get_user_accounts():
            print('\n {}'.format(account))
        selection = input("Account Selection: ")
        while selection not in users_dict[user_name].get_user_accounts():
            input("Please select an account associated with user: ")
        return selection
    else:
        print("No accounts associated with this user yet!")



#     if choice == "add":
#         pass
#     elif choice == "acc":
#         pass #if this is a user account go to account else sat the account doesn't belong to user
#     elif choice =="p":
#         pass
#     elif choice == "n":
#         pass
#     elif choice == "v":
#         pass
#     elif choice == "priv":
#         pass