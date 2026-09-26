def calculate_bill(items):
    """
    Calculate the total shopping bill.

    items should be a list of dictionaries:
    {
        "name": "Notebook",
        "price": 80,
        "quantity": 3
    }
    """

    total = 0

    for item in items:
        total += item["price"] * item["quantity"]

    return f"Total shopping bill: Rs. {total}"