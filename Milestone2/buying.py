"""
buying.py
---------
Handles the supplier restock workflow.

Flow:
    1. Collect supplier name.
    2. Loop — pick medicine → unit type → quantity.
    3. Calculate cost at current rates.
    4. Confirm each addition; ask whether to continue.
    5. Generate purchase document and persist updated stock.

Functions:
    run_restock(stock_list) -> None
"""

from inventory import display_stock, prompt_number, save_stock
from invoice import write_transaction_doc


def _collect_supplier_name():
    """
    Prompt until a non-empty supplier name is entered.

    Returns:
        str: Validated supplier name.
    """
    name = input("\n  Enter supplier / vendor name: ").strip()
    while not name:
        print("  ✗  Supplier name cannot be blank.")
        name = input("  Enter supplier / vendor name: ").strip()
    return name


def _pick_restock_unit():
    """
    Ask whether the restock is being added as tablets or strips.

    Returns:
        str: 'tablet' or 'strip'.
    """
    print("\n  Restock unit:")
    print("    [T]  Tablets (loose)")
    print("    [S]  Strips  (full)")

    while True:
        raw = input("  Choose T or S: ").strip().upper()
        if raw == "T":
            return "tablet"
        if raw == "S":
            return "strip"
        print("  ✗  Enter T for tablet or S for strip only.")


def _tablets_added(unit_type, qty, tabs_per_strip):
    """
    Convert purchased quantity to total tablets for stock update.

    Args:
        unit_type     (str): 'tablet' or 'strip'.
        qty           (int): Number of units purchased.
        tabs_per_strip(int): Tablets in one strip.

    Returns:
        int: Total tablets to add to stock.
    """
    return qty * tabs_per_strip if unit_type == "strip" else qty


def run_restock(stock_list):
    """
    Execute a full supplier restock transaction.

    Collects items to restock, writes a purchase record file,
    and updates medicines.txt with increased stock quantities.

    Args:
        stock_list (list[dict]): The live in-memory inventory.
    """
    supplier    = _collect_supplier_name()
    order       = []
    order_total = 0.0

    while True:
        display_stock(stock_list)

        choice = prompt_number(
            f"  Pick medicine ID to restock (1–{len(stock_list)}) or 0 to finish: ",
            floor=0
        )

        if choice == 0:
            break

        if choice > len(stock_list):
            print(f"  ✗  ID {choice} does not exist. See the table.")
            continue

        target = stock_list[choice - 1]
        print(f"\n  Restocking → {target['med_name']}  ({target['company']})")
        print(f"  Current stock: {target['qty_in_stock']} tablets")

        unit_type = _pick_restock_unit()
        qty       = prompt_number("  How many? ", floor=1)

        # Calculate cost and tablets to add
        rate      = target["strip_price"] if unit_type == "strip" else target["tab_price"]
        line_cost = qty * rate
        to_add    = _tablets_added(unit_type, qty, target["tabs_per_strip"])

        # Update in-memory stock
        target["qty_in_stock"] += to_add

        order.append({
            "item_name": target["med_name"],
            "quantity":  qty,
            "unit_type": unit_type.capitalize() + "s",
            "cost":      line_cost,
        })

        order_total += line_cost

        print(f"\n  ✔  +{to_add} tablets added to {target['med_name']}")
        print(f"  Line cost     : Rs. {line_cost:.2f}")
        print(f"  Running total : Rs. {order_total:.2f}")

        again = input("\n  Add another medicine to restock? (y/n): ").strip().lower()
        if again != "y":
            break

    if not order:
        print("  Nothing was restocked. Operation cancelled.")
        return

    write_transaction_doc("RESTOCK", supplier, order, order_total)
    save_stock(stock_list)
    print("  Inventory updated.\n")
