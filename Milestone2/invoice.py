"""
invoice.py
----------
Generates transaction documents as .txt files.

Each document gets a unique name based on a timestamp.
Two document types are supported:
    - Sales receipt   (txn_type = "SALE")
    - Purchase record (txn_type = "RESTOCK")

Functions:
    write_transaction_doc(txn_type, party_name, line_items, grand_total) -> str
"""

import datetime

_BORDER = "─" * 58
_THICK = "═" * 58


def _build_filename(txn_type):
    """
    Generate a unique filename using transaction type and current timestamp.

    Args:
        txn_type (str): Either 'SALE' or 'RESTOCK'.

    Returns:
        str: Filename like 'SALE_20250508_142301.txt'
    """
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{txn_type}_{stamp}.txt"


def _format_header(f, txn_type, party_name, filename, timestamp):
    """
    Write the top section of the document.

    Args:
        f         : Open file object to write into.
        txn_type  (str): Transaction type label.
        party_name(str): Customer or supplier name.
        filename  (str): Name of this document file.
        timestamp (str): Formatted date and time string.
    """
    f.write(_THICK + "\n")
    f.write("       MEDSTORE PVT. LTD.\n")
    f.write("       Wholesale Medicine Distributor\n")
    f.write(_THICK + "\n")
    f.write(f"  Document  : {filename}\n")
    f.write(f"  Type      : {txn_type}\n")

    label = "Customer" if txn_type == "SALE" else "Supplier"
    f.write(f"  {label:<10}: {party_name}\n")
    f.write(f"  Date/Time : {timestamp}\n")
    f.write(_BORDER + "\n")


def _format_items(f, line_items, txn_type):
    """
    Write each line item in a structured block.

    Args:
        f         : Open file object.
        line_items(list[dict]): Items in this transaction.
        txn_type  (str): 'SALE' or 'RESTOCK'.

    Returns:
        float: Sum of all line totals.
    """
    running_total = 0.0

    for position, item in enumerate(line_items, start=1):
        f.write(f"\n  Item {position}:\n")
        f.write(f"    Medicine   :  {item['item_name']}\n")
        f.write(f"    Quantity   :  {item['quantity']} {item['unit_type']}\n")

        if txn_type == "RESTOCK":
            f.write(
                f"    Rate       :  Rs. {item['cost'] / item['quantity']:.0f} per {item['unit_type']}\n"
            )

        if item.get("discount_amt", 0) > 0:
            original = item["cost"] + item["discount_amt"]
            f.write(f"    Price      :  Rs. {original:.2f}\n")
            f.write(
                f"    Discount   :  Rs. {item['discount_amt']:.2f}  (5% bulk strip offer)\n"
            )
            f.write(f"    Payable    :  Rs. {item['cost']:.2f}\n")
        else:
            f.write(f"    Amount     :  Rs. {item['cost']:.2f}\n")

        f.write("    " + "·" * 36 + "\n")
        running_total += item["cost"]

    return running_total


def write_transaction_doc(txn_type, party_name, line_items, grand_total):
    """
    Create and save a transaction document (.txt) for a sale or restock.

    Args:
        txn_type   (str)      : 'SALE' or 'RESTOCK'.
        party_name (str)      : Customer or supplier name.
        line_items (list[dict]): Each dict needs: item_name, quantity,
                                 unit_type, cost, and optionally discount_amt.
        grand_total (float)   : Pre-calculated total for the transaction.

    Returns:
        str: The filename of the saved document.
    """
    txn_type = txn_type.upper()
    filename = _build_filename(txn_type)
    timestamp = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

    with open(filename, "w", encoding="utf-8") as f:
        _format_header(f, txn_type, party_name, filename, timestamp)
        _format_items(f, line_items, txn_type)

        f.write("\n" + _BORDER + "\n")
        f.write(f"  {'TOTAL ITEMS':<30} {len(line_items):>5}\n")
        f.write(f"  {'GRAND TOTAL':<30} Rs. {grand_total:.2f}\n")
        f.write(_THICK + "\n")

        closing = (
            "Thank you for shopping with us!"
            if txn_type == "SALE"
            else "Stock updated. Thank you, supplier!"
        )
        f.write(f"  {closing}\n")
        f.write(_THICK + "\n")

    print(f"\n  ✔  Document saved  →  {filename}")
    return filename
