from datetime import datetime
import hashlib
import json
from pprint import pp

def load_reviews():
    try:
        with open("reviews.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_reviews(reviews):
    with open("reviews.json", "w") as f:
        json.dump(reviews, f, indent=2)

def get_option(options, prompt="Select an option: ", failed_prompt="That is not an option, try again."):
    for i, o in enumerate(options):
        print(f"{i}: {o}")
    selections = [ str(o) for o in range(len(options)) ]
    while (selection := input(f"{prompt}")) not in selections:
        print(f'{failed_prompt}')
    print() # Newline
    return int(selection)

def parse_statement(filename):
    with open(filename) as file:
        lines = file.readlines()
    transactions = {}
    for line in lines[1:]:
        line = [ item.strip('"\n') for item in line.split(',') ]
        line[0] = datetime.strptime(line[0], '%m/%d/%Y')
        line[1] = datetime.strptime(line[1], '%m/%d/%Y')
        line[6] = float(line[6])
        transaction = (Transaction(*line))
        transactions[transaction.id] = transaction
    return transactions

class Transaction:
    def __init__(self, *values):
        (
            self.transaction_date,
            self.clearing_date,
            self.description,
            self.merchant,
            self.category,
            self.type,
            self.amount,
            self.purchased_by,
        ) = values
        self.fraud = None # None if not reviewed, False if normal transaction, True if its fraud
        # Unique ID
        unique_str = f"{self.transaction_date}{str(self.amount)}{self.description}"
        self.id = hashlib.sha256(unique_str.encode()).hexdigest()

    def __eq__(self, other):
        return isinstance(other, Transaction) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f"{self.transaction_date.date()}, {self.merchant}, {self.amount}"

def read_all_statements(reviews):
    statement_folder = 'statements/'
    filename = 'Apple Card Transactions - April 2025.csv'
    transactions = parse_statement(statement_folder + filename)
    for id, value in reviews.items():
        transactions[id] = value
    return transactions

def view_all(transaction_table):
    transactions = [ transaction for _, transaction in transaction_table.items()]
    for transaction in transactions:
        print(f'{transaction}, {transaction.fraud}')

def review_all(transaction_table):
    # Review Options
    review_options = [
        "Normal Transaction",
        "Fraud",
        "Unknown",
        "Back"
    ]
    review_table = {}

    transactions = [ transaction for _, transaction in transaction_table.items() if transaction.fraud is None ]
    transactions.append('Quit')
    while (option := get_option(transactions, prompt='Select a transaction to review: ')) != len(transactions) - 1:
        transaction = transactions[option]
        print(f'Selected Transaction: {transactions[option]}')
        while (option := get_option(review_options, prompt='Does this transaction look good? ')) != len(review_options) -1:
            selection = review_options[option]
            if selection == "Normal Transaction":
                review_table[transaction.id] = False
                transaction.fraud = False
                transactions.remove(transaction)
            elif selection == "Fraud":
                review_table[transaction.id] = True
                transaction.fraud = True
                transactions.remove(transaction)
            break # we're breaking if we get a valid selection, 
    return {}

def main():
    print("Welcome to a review of your credit card transactions!")
    options = [
        'View All',
        'Review All',
        'Quit',
    ]

    reviews = load_reviews()
    transactions_table = read_all_statements(reviews)
    while options[(option := get_option(options))] != options[-1]:
        if options[option] == 'View All':
            view_all(transactions_table)
        elif options[option] == 'Review All':
            review_all(transactions_table)
    print('Bye bye!')

if __name__ == "__main__":
    main()
