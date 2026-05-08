"""
selling.py
----------
Handles the complete customer sale workflow.

Flow:
    1. Collect customer name.
    2. Loop — pick medicine → unit type → quantity → validate stock.
    3. Apply 5% discount when 2+ strips of the same medicine are purchased.
    4. Confirm each addition; ask whether to continue.
    5. Generate sale document and persist updated stock.

Functions:
    run_sale(stock_list) -> None
"""

from inventory import display_stock, prompt_number, save_stock
from invoice import write_transaction_doc


STRIP_DISCOUNT_RATE    = 0.05
MIN_STRIPS_FOR_DISCOUNT = 2


def _collect_buyer_name():
    """
    Prompt until a non-empty customer name is entered.

    Returns:
        str: Validated customer name.
    """
    name = input("\n  Enter customer name: ").strip()
    while not name:
        print("  ✗  Name cannot be blank.")
        name = input("  Enter customer name: ").strip()
    return name


def _pick_medicine(stock_list):
    """
    Show inventory and return the chosen medicine dict.
    Returns None if the user types 0 to stop.

    Args:
        stock_list (list[dict]): Current inventory.

    Returns:
        dict | None: Selected medicine, or None if user exits.
    """
    display_stock(stock_list)
    choice = prompt_number(
        f"  Pick medicine ID (1–{len(stock_list)}) or 0 to finish: ",
        floor=0
    )

    if choice == 0:
        return None

    if choice > len(stock_list):
        print(f"  ✗  No medicine with ID {choice}. Check the table above.")
        return _pick_medicine(stock_list)   # recurse until valid

    return stock_list[choice - 1]


def _pick_unit_type():
    """
    Ask whether the sale is by tablet or strip.

    Returns:
        str: 'tablet' or 'strip'.
    """
    print("\n  Unit type:")
    print("    [T]  Tablet")
    print("    [S]  Strip")

    while True:
        raw = input("  Choose T or S: ").strip().upper()
        if raw == "T":
            return "tablet"
        if raw == "S":
            return "strip"
        print("  ✗  Enter T for tablet or S for strip.")


def _calculate_sale_line(med, unit_type, qty):
    """
    Compute the cost and discount for one sale line item.

    Discount rule: 5% off when buying 2 or more strips of the same medicine.

    Args:
        med       (dict): Medicine record.
        unit_type (str) : 'tablet' or 'strip'.
        qty       (int) : Number of tablets or strips.

    Returns:
        tuple(float, float): (final_cost, discount_amount)
    """
    if unit_type == "tablet":
        return qty * med["tab_price"], 0.0

    gross    = qty * med["strip_price"]
    discount = gross * STRIP_DISCOUNT_RATE if qty >= MIN_STRIPS_FOR_DISCOUNT else 0.0
    return gross - discount, discount


def run_sale(stock_list):
    """
    Execute a full customer sale transaction.

    Collects items into a bill, applies discounts where applicable,
    writes a sale receipt file, and updates medicines.txt.

    Args:
        stock_list (list[dict]): The live in-memory inventory.
    """
    buyer = _collect_buyer_name()
    bill        = []
    bill_total  = 0.0

    while True:
        chosen_med = _pick_medicine(stock_list)
        if chosen_med is None:
            break   # user typed 0 — done adding items

        print(f"\n  Selected → {chosen_med['med_name']}  ({chosen_med['company']})")

        unit_type = _pick_unit_type()
        qty       = prompt_number("  How many? ", floor=1)

        # Stock validation
        tabs_required = qty * chosen_med["tabs_per_strip"] if unit_type == "strip" else qty

        if tabs_required > chosen_med["qty_in_stock"]:
            if unit_type == "strip":
                available = chosen_med["qty_in_stock"] // chosen_med["tabs_per_strip"]
                print(f"  ✗  Only {available} full strip(s) available ({chosen_med['qty_in_stock']} tablets).")
            else:
                print(f"  ✗  Only {chosen_med['qty_in_stock']} tablet(s) in stock.")
            continue

        cost, discount = _calculate_sale_line(chosen_med, unit_type, qty)

        # Deduct from in-memory stock
        chosen_med["qty_in_stock"] -= tabs_required

        bill.append({
            "item_name":    chosen_med["med_name"],
            "quantity":     qty,
            "unit_type":    unit_type.capitalize() + "s",
            "cost":         cost,
            "discount_amt": discount,
        })

        bill_total += cost

        print(f"\n  ✔  Added — Rs. {cost:.2f}", end="")
        if discount > 0:
            print(f"  (saved Rs. {discount:.2f} on bulk strips)", end="")
        print(f"\n  Running total: Rs. {bill_total:.2f}")

        again = input("\n  Add another item? (y/n): ").strip().lower()
        if again != "y":
            break

    if not bill:
        print("  No items were added. Sale cancelled.")
        return

    write_transaction_doc("SALE", buyer, bill, bill_total)
    save_stock(stock_list)
    print("  Inventory updated.\n")
