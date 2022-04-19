from datetime import datetime
from tinkoff.invest import Client
import datetime
import pandas as pd

"""
DOCs:
https://tinkoff.github.io/investAPI
https://github.com/Tinkoff/invest-python
"""


def main():
    token_read_only_1 = ""
    # Put your token in format "..."
    account_id = ""  # Put your account ID in format "..."
    ### To find your account ID use get_accounts (func. accounts) ###

    answ = ""  # additional variable for switch-case construction

    with Client(token_read_only_1) as client:

        while (answ != "4"):
            print('\n', "What would you like to do? (Write: '1' / '2' / '3' / '4') ")
            print("1) Watch your brokerage accounts ")
            print("2) Watch your transactions ")
            print(
                "3) Watch your portfolio content and value (at current exchange rates) ")
            print("4) exit ")
            answ = input()
            match answ:  # switch-case construction (for Python 3.10 and more)
                case "1":
                    print('\n', "Your brokerage accounts: ")
                    accounts(client)
                    breakpoint
                case "2":
                    print('\n', "Your transactions: ")
                    operations(client, account_id)
                    breakpoint
                case "3":
                    print(
                        '\n', "Portfolio content and value (at current exchange rates): ")
                    value(client, account_id)
                    breakpoint


def accounts(c):  # Show all brokerage accounts and their details
    print(c.users.get_accounts())


def operations(c, id):  # Display all operations on the brokerage account in the time interval
    print(c.operations.get_operations(  # List of shares
        account_id=id,
        from_=datetime.datetime(2021, 1, 1),
        to=datetime.datetime.now()))


def value(c, id):  # Display portfolio contents and value
    # Conversion of custom data type to string
    #t_string = str(c.operations.get_portfolio(account_id=id))
    #t_string.replace("),", "\n")
    #t_string.split("), ")
    # print((c.operations.get_portfolio(account_id=id)))
    # for temp in t_string:
    #     t_string.replace("PortfolioResponse", "\n")
    #     print(temp)
    # print(t_string)
    #r : p_response = c.operations.get_portfolio(account_id=id)
    keys = ['total_amount_shares', 'total_amount_bonds',
            'total_amount_etf', 'total_amount_currencies', 'total_amount_futures']
    data = str({k: getattr(c.operations.get_portfolio(account_id=id), k)
               for k in keys})  # formal output with keys
    print(data)


def cost_money(m):  # Function to convert custom currency format to Float
    return (m.units + m.nano / 1e9)  # nano is 10^-9


main()
