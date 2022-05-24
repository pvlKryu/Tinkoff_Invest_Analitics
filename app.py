from datetime import datetime
from tinkoff.invest import Client, RequestError, PositionsResponse, AccessLevel, OperationsResponse, Operation, \
    OperationState, OperationType
from tinkoff.invest.services import Services

import datetime
import pandas as pd

"""
DOCs:
https://tinkoff.github.io/investAPI
https://github.com/Tinkoff/invest-python
"""

"""
Добавить считывание токена от пользователя и авто получение его account_id
"""

def main():
    token_read_only_1 = ""
    # Put your token in format "..."
    account_id = ""  # Put your account ID in format "..."
    ### To find your account ID use get_accounts (func. accounts 1) ) ###

    answ = ""  # additional variable for switch-case construction

    with Client(token_read_only_1) as client:

        while (answ != "0"):
            print('\n', "What would you like to do? (Write: '1' / '2' / '3' / '4') ")
            print("1) Watch your brokerage accounts (+ID's) ")
            print("2) Watch your transactions ")
            print("3) Watch your portfolio content and value (at current exchange rates) ")
            print("4) Portfolio basic statistics: ")
            print("5) Broker report: ") #Not finished
            #...#
            print("0) exit ")
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
                        '\n', "Portfolio content and value: ", '\n')
                    value(client, account_id)
                    breakpoint
                case "4":
                    print(
                        '\n', "Portfolio basic statistics: ")
                    basic_statistics(client, account_id)
                    breakpoint

                case "5": #In procees 
                    print(
                        '\n', "Broker report: ")
                    broker_report(client, account_id)
                    breakpoint



def accounts(c):  # Show all brokerage accounts and their details
    r = c.users.get_accounts() 
    d = []

    for acc in r.accounts:
        if acc.type == 0:
            acc.type = 'Unknown'
        elif acc.type == 1:
            acc.type = 'Brokerage account'
        elif acc.type == 2:
            acc.type = 'IIS'
        else:
            acc.type = 'Investkopilka'

        acc.opened_date = acc.opened_date.strftime('%B %d, %Y')
        acc.closed_date = acc.closed_date.strftime('%B %d, %Y')

        if (acc.closed_date == 'January 01, 1970'):
            acc.closed_date = 'Not closed'

        if acc.status == 0:
                acc.status = 'Unknown'
        elif acc.status == 1:
            acc.status = 'opening'
        elif acc.status == 2:
            acc.status = 'Opened'
        else:
            acc.status = 'Closed'

        if acc.access_level == 0:
                acc.access_level = 'Unknown'
        elif acc.access_level == 1:
            acc.access_level = 'Full access'
        elif acc.access_level == 2:
            acc.access_level = 'Reading only'
        else:
            acc.access_level = 'No access'
        
        d.append(acc)

    d = pd.DataFrame(d, columns=('id', 'type', 'name', 'status', 'opened_date', 'closed_date', 'access_level'))

    print(d)


def operations(c, id):  # Display all operations on the brokerage account in the time interval
    r = c.operations.get_operations(
        account_id=id,
        from_=datetime.datetime(2021, 1, 1),
        to=datetime.datetime.now())
    
    d = []

    for op in r.operations:
        op.payment = float(cost_money(op.payment))
        op.price = float(cost_money(op.price))

        if op.state == 0:
                op.state = 'Unknown'
        elif op.state == 1:
            op.state = 'Done'
        else:
            op.state = 'Cancelled'

        d.append(op) 

    d = pd.DataFrame(d, columns=('currency', 'payment', 'price', 'state', 'quantity_rest', 'figi', 'instrument_type', 'date', 'type'))

    print(d)


def value(c, id):  # Display portfolio contents and value
    d = {}
    r = c.operations.get_portfolio(account_id=id)
    keys1 = ['total_amount_shares', 'total_amount_bonds', 'total_amount_etf', 'total_amount_currencies', 'total_amount_futures']
    p_response = {k: getattr(r, k) for k in keys1} 
    #type p_response - dict
    for keys1 in p_response:
        p_response[keys1] = cost_money(p_response[keys1])
        d[keys1] = p_response[keys1]

    d = pd.DataFrame.from_dict(d, orient='index', columns=['Total cost (rub)'])

    print('General table:', '\n', d, '\n')

    p = c.operations.get_positions(account_id=id)
    keys2 = ['securities', 'money']
    for k in keys2:
        tmp = getattr(p, k)
        #type(tmp) - list
        df2 = pd.DataFrame(tmp)
        table = df2.to_string(index=False)
        print()
        print(k, 'table:')
        print(table, '\n')
    #Перевести денежный формат в money table

def basic_statistics(c, id):
    r = c.operations.get_portfolio(account_id=id)
    print(r)

def broker_report(c, id):
    pass
 

def cost_money(m):  # Function to convert custom currency format to Float
    return (m.units + m.nano / 1e9)  # nano is 10^-9


main()
