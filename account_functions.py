import csv, email, smtplib

def deposit(accounts_dict, account_name):
    deposit = input("How much would you like to deposit: ")
    while not deposit.isnumeric():
        deposit = input("Please enter a number to deposit: ")
    accounts_dict[account_name].make_deposit(int(deposit)) # what about cents?

def withdrawal(accounts_dict, account_name):
    withdrawal = input("How much would you like to withdrawal?: ")
    while not withdrawal.isnumeric():
        withdrawal = input("Please Enter a number: ")
    if accounts_dict[account_name].get_value() < int(withdrawal):
        print(f"\nInsufficient funds to make withdrawal\nMaximum withdrawal is {accounts_dict[account_name].get_value()}")
    else:
        accounts_dict[account_name].make_withdrawal(int(withdrawal))

def set_password(accounts_dict, account_name):
    if accounts_dict[account_name].get_password() == 'unset':
        password = input("Enter new password: ")
        accounts_dict[account_name].set_password(password)
    else:
        current_pw = input("Please enter current password: ")
        if current_pw == accounts_dict[account_name].get_password():
            new_pw = input("Enter new password: ")
            accounts_dict[account_name].set_password(new_pw)

def delete_account(accounts_dict, account_name):
    if "y" == input(f"Are you sure you want to delete {account_name}? y/n: "):
        accounts_dict.pop(account_name)
        print(f'{account_name} deleted')

def export_logs_as_csv(log_dict, account_name):
    with open(f'{account_name}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Type of Transaction', 'Amount'])
        for key in log_dict[account_name].get_account_log().keys():
            writer.writerow([f'{key}, {log_dict[account_name].get_account_log()[key][0]}, {log_dict[account_name].get_account_log()[key][1]}'])

def email_account(accounts_dict, account_name):
    address = input("Enter email address: ")
    message = email.message.EmailMessage()
    message["From"] = account_name
    message["To"] = address
    message["Subject"] = f'{account_name} account log'
    message.set_content(accounts_dict)
    server = smtplib.SMTP('localhost')
    server.send_message(message)
    server.quit()
    
    