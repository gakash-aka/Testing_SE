class ATM:
    def __init__(self, balance=10000):
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid amount"

        if amount % 100 != 0:
            return "Amount must be a multiple of 100"

        if amount > 5000:
            return "Daily withdrawal limit exceeded"

        if amount > self.balance:
            return "Insufficient balance"

        self.balance -= amount

        return f"Withdrawal successful. Remaining balance: {self.balance}"

    def deposit(self, amount):
        if amount <= 0:
            return "Invalid deposit amount"

        self.balance += amount

        return f"Deposit successful. Balance: {self.balance}"

    def check_balance(self):
        return f"Current balance: {self.balance}"


def atm_transaction(balance, transaction, amount=0):
    atm = ATM(balance)

    if transaction == "withdraw":
        return atm.withdraw(amount)

    elif transaction == "deposit":
        return atm.deposit(amount)

    elif transaction == "balance":
        return atm.check_balance()

    else:
        return "Invalid transaction"