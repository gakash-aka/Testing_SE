import pytest

from login import (
    calculate_discount,
    calculate_tax,
    calculate_shipping,
    process_cart,
    make_payment,
    checkout,
    InvalidQuantityError,
    InsufficientStockError,
    InvalidPaymentError
)


# ------------------------------------------------
# DISCOUNT TESTS
# ------------------------------------------------

def test_premium_discount_5000():
    assert calculate_discount(
        5000, "premium"
    ) == 1000


def test_premium_discount_2000():
    assert calculate_discount(
        2000, "premium"
    ) == 300


def test_premium_discount_1000():
    assert calculate_discount(
        1000, "premium"
    ) == 100


def test_premium_no_discount():
    assert calculate_discount(
        500, "premium"
    ) == 0


def test_regular_discount_5000():
    assert calculate_discount(
        5000, "regular"
    ) == 500


def test_regular_discount_2000():
    assert calculate_discount(
        2000, "regular"
    ) == 100


def test_regular_no_discount():
    assert calculate_discount(
        1000, "regular"
    ) == 0


def test_invalid_customer_type():
    with pytest.raises(ValueError):
        calculate_discount(
            5000, "student"
        )


def test_negative_total():
    with pytest.raises(ValueError):
        calculate_discount(
            -100, "regular"
        )


# ------------------------------------------------
# TAX TESTS
# ------------------------------------------------

def test_high_tax():
    assert calculate_tax(5000) == 900


def test_medium_tax():
    assert calculate_tax(2000) == 240


def test_low_tax():
    assert calculate_tax(1000) == 50


def test_negative_tax():
    with pytest.raises(ValueError):
        calculate_tax(-500)


# ------------------------------------------------
# SHIPPING TESTS
# ------------------------------------------------

def test_premium_free_shipping():
    assert calculate_shipping(
        500, "premium"
    ) == 0


def test_regular_free_shipping():
    assert calculate_shipping(
        3000, "regular"
    ) == 0


def test_regular_50_shipping():
    assert calculate_shipping(
        1500, "regular"
    ) == 50


def test_regular_100_shipping():
    assert calculate_shipping(
        500, "regular"
    ) == 100


# ------------------------------------------------
# CART TESTS
# ------------------------------------------------

def test_empty_cart():

    with pytest.raises(ValueError):
        process_cart(
            [],
            "regular"
        )


def test_missing_name():

    cart = [
        {
            "price": 100,
            "quantity": 1,
            "stock": 5
        }
    ]

    with pytest.raises(ValueError):
        process_cart(
            cart,
            "regular"
        )


def test_missing_price():

    cart = [
        {
            "name": "Pen",
            "quantity": 1,
            "stock": 5
        }
    ]

    with pytest.raises(ValueError):
        process_cart(
            cart,
            "regular"
        )


def test_missing_quantity():

    cart = [
        {
            "name": "Pen",
            "price": 100,
            "stock": 5
        }
    ]

    with pytest.raises(ValueError):
        process_cart(
            cart,
            "regular"
        )


def test_missing_stock():

    cart = [
        {
            "name": "Pen",
            "price": 100,
            "quantity": 1
        }
    ]

    with pytest.raises(ValueError):
        process_cart(
            cart,
            "regular"
        )


def test_invalid_price():

    cart = [
        {
            "name": "Pen",
            "price": 0,
            "quantity": 1,
            "stock": 5
        }
    ]

    with pytest.raises(ValueError):
        process_cart(
            cart,
            "regular"
        )


def test_invalid_quantity():

    cart = [
        {
            "name": "Pen",
            "price": 100,
            "quantity": 0,
            "stock": 5
        }
    ]

    with pytest.raises(InvalidQuantityError):
        process_cart(
            cart,
            "regular"
        )


def test_negative_quantity():

    cart = [
        {
            "name": "Pen",
            "price": 100,
            "quantity": -1,
            "stock": 5
        }
    ]

    with pytest.raises(InvalidQuantityError):
        process_cart(
            cart,
            "regular"
        )


def test_insufficient_stock():

    cart = [
        {
            "name": "Laptop",
            "price": 50000,
            "quantity": 10,
            "stock": 5
        }
    ]

    with pytest.raises(InsufficientStockError):
        process_cart(
            cart,
            "regular"
        )


# ------------------------------------------------
# BULK QUANTITY TESTS
# ------------------------------------------------

def test_bulk_quantity_10():

    cart = [
        {
            "name": "Pen",
            "price": 100,
            "quantity": 10,
            "stock": 20
        }
    ]

    result = process_cart(
        cart,
        "regular"
    )

    assert result["subtotal"] == 900


def test_bulk_quantity_5():

    cart = [
        {
            "name": "Pen",
            "price": 100,
            "quantity": 5,
            "stock": 10
        }
    ]

    result = process_cart(
        cart,
        "regular"
    )

    assert result["subtotal"] == 475


def test_normal_quantity():

    cart = [
        {
            "name": "Pen",
            "price": 100,
            "quantity": 2,
            "stock": 10
        }
    ]

    result = process_cart(
        cart,
        "regular"
    )

    assert result["subtotal"] == 200


# ------------------------------------------------
# PAYMENT TESTS
# ------------------------------------------------

def test_cash_payment():

    result = make_payment(
        1000,
        1200,
        "cash"
    )

    assert result["status"] == "Payment Successful"
    assert result["change"] == 200


def test_card_payment():

    result = make_payment(
        1000,
        1000,
        "card"
    )

    assert result["status"] == "Payment Successful"
    assert result["change"] == 0


def test_upi_payment():

    result = make_payment(
        1000,
        1000,
        "upi"
    )

    assert result["status"] == "Payment Successful"
    assert result["change"] == 0


def test_insufficient_payment():

    with pytest.raises(InvalidPaymentError):

        make_payment(
            1000,
            500,
            "cash"
        )


def test_negative_payment():

    with pytest.raises(InvalidPaymentError):

        make_payment(
            1000,
            -100,
            "cash"
        )


def test_invalid_payment_method():

    with pytest.raises(InvalidPaymentError):

        make_payment(
            1000,
            1000,
            "bitcoin"
        )


def test_card_overpayment():

    with pytest.raises(InvalidPaymentError):

        make_payment(
            1000,
            1200,
            "card"
        )


def test_upi_overpayment():

    with pytest.raises(InvalidPaymentError):

        make_payment(
            1000,
            1200,
            "upi"
        )


# ------------------------------------------------
# COMPLETE CHECKOUT TEST
# ------------------------------------------------

def test_complete_checkout():

    cart = [
        {
            "name": "Laptop",
            "price": 50000,
            "quantity": 1,
            "stock": 5
        },
        {
            "name": "Mouse",
            "price": 1000,
            "quantity": 2,
            "stock": 10
        }
    ]

    result = checkout(
        cart,
        "premium",
        55000,
        "card"
    )

    assert result["payment"]["status"] == \
        "Payment Successful"

    assert result["payment"]["change"] == 0