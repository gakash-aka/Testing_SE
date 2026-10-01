class ShoppingError(Exception):
    pass


class InvalidQuantityError(ShoppingError):
    pass


class InsufficientStockError(ShoppingError):
    pass


class InvalidPaymentError(ShoppingError):
    pass


def calculate_discount(total, customer_type):
    """
    Calculate discount based on total amount and customer type.
    """

    if total < 0:
        raise ValueError("Total cannot be negative")

    if customer_type == "premium":

        if total >= 5000:
            return total * 0.20

        elif total >= 2000:
            return total * 0.15

        elif total >= 1000:
            return total * 0.10

        else:
            return 0

    elif customer_type == "regular":

        if total >= 5000:
            return total * 0.10

        elif total >= 2000:
            return total * 0.05

        else:
            return 0

    else:
        raise ValueError("Invalid customer type")


def calculate_tax(amount):
    """
    Calculate GST based on amount.
    """

    if amount < 0:
        raise ValueError("Amount cannot be negative")

    if amount >= 5000:
        tax_rate = 0.18

    elif amount >= 2000:
        tax_rate = 0.12

    else:
        tax_rate = 0.05

    return amount * tax_rate


def calculate_shipping(amount, customer_type):
    """
    Calculate shipping charges.
    """

    if customer_type == "premium":
        return 0

    if amount >= 3000:
        return 0

    elif amount >= 1000:
        return 50

    else:
        return 100


def process_cart(cart, customer_type):
    """
    Process products in the shopping cart.

    cart format:
    [
        {
            "name": "Laptop",
            "price": 50000,
            "quantity": 1,
            "stock": 5
        }
    ]
    """

    if not cart:
        raise ValueError("Cart is empty")

    subtotal = 0

    for product in cart:

        if "name" not in product:
            raise ValueError("Product name missing")

        if "price" not in product:
            raise ValueError("Product price missing")

        if "quantity" not in product:
            raise ValueError("Product quantity missing")

        if "stock" not in product:
            raise ValueError("Product stock missing")

        name = product["name"]
        price = product["price"]
        quantity = product["quantity"]
        stock = product["stock"]

        if price <= 0:
            raise ValueError(
                f"Invalid price for {name}"
            )

        if quantity <= 0:
            raise InvalidQuantityError(
                f"Invalid quantity for {name}"
            )

        if quantity > stock:
            raise InsufficientStockError(
                f"Insufficient stock for {name}"
            )

        item_total = price * quantity

        # Bulk purchase discount
        if quantity >= 10:
            item_total = item_total * 0.90

        elif quantity >= 5:
            item_total = item_total * 0.95

        subtotal += item_total

    discount = calculate_discount(
        subtotal,
        customer_type
    )

    amount_after_discount = subtotal - discount

    tax = calculate_tax(
        amount_after_discount
    )

    shipping = calculate_shipping(
        amount_after_discount,
        customer_type
    )

    final_amount = (
        amount_after_discount
        + tax
        + shipping
    )

    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "final_amount": round(final_amount, 2)
    }


def make_payment(amount, paid_amount, payment_method):
    """
    Process customer payment.
    """

    if amount <= 0:
        raise ValueError("Invalid bill amount")

    if paid_amount < 0:
        raise InvalidPaymentError(
            "Payment cannot be negative"
        )

    if payment_method not in [
        "cash",
        "card",
        "upi"
    ]:
        raise InvalidPaymentError(
            "Invalid payment method"
        )

    if paid_amount < amount:
        raise InvalidPaymentError(
            "Insufficient payment"
        )

    if payment_method == "cash":

        change = paid_amount - amount

    elif payment_method == "card":

        if paid_amount != amount:
            raise InvalidPaymentError(
                "Card payment must match bill amount"
            )

        change = 0

    else:  # UPI

        if paid_amount != amount:
            raise InvalidPaymentError(
                "UPI payment must match bill amount"
            )

        change = 0

    return {
        "status": "Payment Successful",
        "change": round(change, 2)
    }


def checkout(cart, customer_type, paid_amount, payment_method):
    """
    Complete shopping checkout.
    """

    bill = process_cart(
        cart,
        customer_type
    )

    payment = make_payment(
        bill["final_amount"],
        paid_amount,
        payment_method
    )

    return {
        "bill": bill,
        "payment": payment
    }