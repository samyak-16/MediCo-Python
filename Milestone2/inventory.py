"""
inventory.py
------------
Manages reading, saving, and displaying the medicine inventory file.

All medicine records are stored as dicts with these keys:
    med_name, company, qty_in_stock, tab_price, strip_price, tabs_per_strip

Functions:
    load_stock()                  -> list[dict]
    save_stock(list)              -> None
    display_stock(list)           -> None
    prompt_number(msg, floor)     -> int
"""

STOCK_FILE = "medicines.txt"

# Column widths for the display table
_COL = {
    "id":    4,
    "name":  24,
    "brand": 20,
    "stock": 12,
    "t_rate": 11,
    "s_rate": 12,
    "tps":    10,
}


def load_stock():
    """
    Parse medicines.txt into a list of medicine dictionaries.

    Each line must have exactly 6 comma-separated values:
        name, brand, stock(tablets), tablet_rate, strip_rate, tabs_per_strip

    Returns:
        list[dict]: Parsed medicine records.

    Raises:
        FileNotFoundError: Propagated if medicines.txt is missing.
    """
    records = []

    with open(STOCK_FILE, "r") as file_handle:
        for row_index, raw_line in enumerate(file_handle, start=1):
            clean = raw_line.strip()
            if not clean:
                continue

            fields = clean.split(",")
            if len(fields) != 6:
                print(f"  ⚠  Row {row_index} ignored — expected 6 fields, found {len(fields)}.")
                continue

            try:
                entry = {
                    "med_name":       fields[0].strip(),
                    "company":        fields[1].strip(),
                    "qty_in_stock":   int(fields[2].strip()),
                    "tab_price":      int(fields[3].strip()),
                    "strip_price":    int(fields[4].strip()),
                    "tabs_per_strip": int(fields[5].strip()),
                }
                records.append(entry)
            except ValueError:
                print(f"  ⚠  Row {row_index} ignored — numeric fields could not be parsed.")

    return records


def save_stock(med_list):
    """
    Overwrite medicines.txt with the current in-memory inventory.

    Args:
        med_list (list[dict]): Full medicine inventory to persist.
    """
    with open(STOCK_FILE, "w") as file_handle:
        for rec in med_list:
            line = (
                f"{rec['med_name']}, {rec['company']}, {rec['qty_in_stock']}, "
                f"{rec['tab_price']}, {rec['strip_price']}, {rec['tabs_per_strip']}\n"
            )
            file_handle.write(line)


def display_stock(med_list):
    """
    Render the medicine inventory as a formatted table with row IDs.

    Args:
        med_list (list[dict]): Medicine records to display.
    """
    if not med_list:
        print("  No medicines currently in inventory.")
        return

    w = _COL
    total_width = sum(w.values()) + len(w) * 3

    # Header
    print()
    print("  ┌" + "─" * total_width + "┐")
    header = (
        f"  │ {'#':<{w['id']}} "
        f"{'Medicine':<{w['name']}} "
        f"{'Brand':<{w['brand']}} "
        f"{'Stock':>{w['stock']}} "
        f"{'Rs/Tab':>{w['t_rate']}} "
        f"{'Rs/Strip':>{w['s_rate']}} "
        f"{'Tabs/Strip':>{w['tps']}} │"
    )
    print(header)
    print("  ├" + "─" * total_width + "┤")

    for idx, med in enumerate(med_list, start=1):
        row = (
            f"  │ {str(idx):<{w['id']}} "
            f"{med['med_name']:<{w['name']}} "
            f"{med['company']:<{w['brand']}} "
            f"{str(med['qty_in_stock']):>{w['stock']}} "
            f"{str(med['tab_price']):>{w['t_rate']}} "
            f"{str(med['strip_price']):>{w['s_rate']}} "
            f"{str(med['tabs_per_strip']):>{w['tps']}} │"
        )
        print(row)

    print("  └" + "─" * total_width + "┘")
    print()


def prompt_number(message, floor=0):
    """
    Repeatedly prompt until the user enters an integer >= floor.

    Args:
        message (str): Input prompt shown to the user.
        floor   (int): Minimum acceptable value (default 0).

    Returns:
        int: Validated integer input.
    """
    while True:
        raw = input(message).strip()
        try:
            value = int(raw)
            if value < floor:
                print(f"  ✗  Must be {floor} or higher. Try again.")
            else:
                return value
        except ValueError:
            print(f"  ✗  '{raw}' is not a valid number. Please try again.")
