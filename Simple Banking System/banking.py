from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")


def Start():
    global balance_logout
    balance_logout = 1
    while True:
        print("""1. Create an account
2. Log into account
0. Exit""")
        create_login = int(input())
        print('')
        
        if create_login == 1:    
            CreateAccount()
        elif create_login == 2:
            LogIn()
        elif create_login == 0:
            break
        if balance_logout == 0:
            break
            
        
def CreateAccount():
    account = "400000"
    password = ""
    acumulative_num = 8
    for i in range(0, 9):
        random_num = randint(0, 9)
        account += str(random_num)
        if i % 2 == 0:
            if random_num > 4:
                acumulative_num += random_num * 2 - 9
            else:
                acumulative_num += random_num * 2
        else:
            acumulative_num += random_num
    account += str((10 - acumulative_num % 10) % 10)
    for i in range(0, 4):
        password += str(randint(0, 9))
    cur.execute("INSERT INTO card (number, pin) VALUES (?,?)", (account, password))
    conn.commit()
    print(f'''Your card has been created
Your card number:
{account}
Your card PIN:
{password}
''')
        
def LogIn():
    print('Enter your card number:')
    log_account = input()
    print('Enter your PIN:')
    log_password = input()
    cur.execute("SELECT number, pin, balance FROM card WHERE number=?", (log_account,))
    records = cur.fetchall()
    print('')
    if records == []:
        print('Wrong card number or PIN!\n')
    else:
        if log_account == records[0][0] and log_password == records[0][1]:
            print('You have successfully logged in!\n')
            AccountManagement(records[0][0])
        else:
            print('Wrong card number or PIN!\n')
    
def AccountManagement(account):
    while True:
        global balance_logout
        cur.execute('SELECT balance FROM card WHERE number=?', (account,))
        acc_balance = cur.fetchall()
        acc_balance = acc_balance[0][0]
        print('''1. Balance        
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
        balance_logout = int(input())
        print('')
        if balance_logout == 1:
            print(f'Balance: {acc_balance}\n')
        if balance_logout == 2:
            add_income(account, acc_balance)
        if balance_logout == 3:
            do_transfer(account, acc_balance)
        if balance_logout == 4:
            close_account(account)
            break
        if balance_logout == 5:
            print('\nYou have successfully logged out!\n')
            break
        if balance_logout == 0:
            break        

def add_income(acc_number, acc_balance):
    print('Enter income:')
    income = int(input())
    print('Income was added!\n')
    cur.execute("UPDATE card SET balance=? WHERE number=?", (str(acc_balance + income), acc_number,))
    conn.commit()

def do_transfer(acc_number, acc_balance):
    print('Transfer')
    transfer_card_number = input('Enter card number:\n')
    if not Luhn_algorithm_test(transfer_card_number):
        print('Probably you made mistake in the card number. Please try again!')
        return
    if transfer_card_number == acc_number:
        print("You can't transfer money to the same account!")
        return
    cur.execute("SELECT number, balance FROM card WHERE number=?", (transfer_card_number,))
    records = cur.fetchall()
    if records == []:
        print('Such a card does not exist.\n')
    else:
        transfer_money = int(input('Enter how much money you want to transfer:\n'))
        if transfer_money > acc_balance:
            print('Not enough money!')
        else:
            cur.execute("UPDATE card SET balance=? WHERE number=?", (str(acc_balance - transfer_money), acc_number,))
            conn.commit()
            cur.execute("UPDATE card SET balance=? WHERE number=?", (str(records[0][1] + transfer_money), transfer_card_number,))
            conn.commit()
            print('Sucess!')

def Luhn_algorithm_test(account):
    acumulative = 0
    for i in range(0, 15):
        single_number = int(account[i])
        if (i + 1) % 2 != 0:
            if single_number > 4:
                acumulative += single_number * 2 - 9
            else:
                acumulative += single_number * 2
        else:
            acumulative += single_number
    if int(account[15]) == (10 - (acumulative % 10)) %10:
        return True
    return False

def close_account(account):
    cur.execute('DELETE FROM card WHERE number=?', (account,))
    conn.commit()
    print('The account has been closed!\n')

Start()

print('Bye!')