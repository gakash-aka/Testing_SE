import pytest

from black_box_testing import ATM
from black_box_testing import atm_transaction


# -----------------------------------------
# WITHDRAWAL TESTS
# -----------------------------------------

def test_valid_withdrawal():

    atm = ATM(10000)

    result = atm.withdraw(2000)

    assert result == \
        "Withdrawal successful. Remaining balance: 8000"


def test_small_withdrawal():

    atm = ATM(10000)

    result = atm.withdraw(100)

    assert result == \
        "Withdrawal successful. Remaining balance: 9900"


def test_withdrawal_5000():

    atm = ATM(10000)

    result = atm.withdraw(5000)

    assert result == \
        "Withdrawal successful. Remaining balance: 5000"


def test_withdrawal_above_limit():

    atm = ATM(10000)

    result = atm.withdraw(5100)

    assert result == \
        "Daily withdrawal limit exceeded"


def test_withdrawal_zero():

    atm = ATM(10000)

    result = atm.withdraw(0)

    assert result == "Invalid amount"


def test_negative_withdrawal():

    atm = ATM(10000)

    result = atm.withdraw(-500)

    assert result == "Invalid amount"


def test_non_multiple_withdrawal():

    atm = ATM(10000)

    result = atm.withdraw(550)

    assert result == \
        "Amount must be a multiple of 100"


def test_insufficient_balance():

    atm = ATM(1000)

    result = atm.withdraw(2000)

    assert result == "Insufficient balance"


# -----------------------------------------
# DEPOSIT TESTS
# -----------------------------------------

def test_valid_deposit():

    atm = ATM(5000)

    result = atm.deposit(2000)

    assert result == \
        "Deposit successful. Balance: 7000"


def test_small_deposit():

    atm = ATM(5000)

    result = atm.deposit(100)

    assert result == \
        "Deposit successful. Balance: 5100"


def test_zero_deposit():

    atm = ATM(5000)

    result = atm.deposit(0)

    assert result == "Invalid deposit amount"


def test_negative_deposit():

    atm = ATM(5000)

    result = atm.deposit(-1000)

    assert result == "Invalid deposit amount"


# -----------------------------------------
# BALANCE TESTS
# -----------------------------------------

def test_check_balance():

    atm = ATM(7500)

    result = atm.check_balance()

    assert result == "Current balance: 7500"


def test_zero_balance():

    atm = ATM(0)

    result = atm.check_balance()

    assert result == "Current balance: 0"


# -----------------------------------------
# ATM TRANSACTION TESTS
# -----------------------------------------

def test_transaction_withdraw():

    result = atm_transaction(
        10000,
        "withdraw",
        1000
    )

    assert result == \
        "Withdrawal successful. Remaining balance: 9000"


def test_transaction_deposit():

    result = atm_transaction(
        5000,
        "deposit",
        2000
    )

    assert result == \
        "Deposit successful. Balance: 7000"


def test_transaction_balance():

    result = atm_transaction(
        8000,
        "balance"
    )

    assert result == \
        "Current balance: 8000"


def test_invalid_transaction():

    result = atm_transaction(
        5000,
        "transfer",
        1000
    )

    assert result == "Invalid transaction"


# -----------------------------------------
# BOUNDARY VALUE TESTING
# -----------------------------------------

def test_withdrawal_boundary_100():

    atm = ATM(10000)

    result = atm.withdraw(100)

    assert "successful" in result


def test_withdrawal_boundary_5000():

    atm = ATM(10000)

    result = atm.withdraw(5000)

    assert "successful" in result


def test_withdrawal_boundary_5100():

    atm = ATM(10000)

    result = atm.withdraw(5100)

    assert result == \
        "Daily withdrawal limit exceeded"