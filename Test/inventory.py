"""
inventory.py
------------
Handles all reading, writing, and display of the medicines inventory file.

Functions:
    read_medicines()            -> list[dict]
    save_all_medicines(list)    -> None
    show_inventory(list)        -> None
    ask_for_number(msg, min)    -> int
"""

DB_FILENAME = "medicines.txt"


def read_medicines():
    """
    Read medicines.txt and return a list of medicine dictionaries.

    File format (comma-separated, 6 columns):
        medicine_name, brand, stock_in_tablets, rate_per_tablet,
        rate_per_strip, tablets_per_strip

    Returns:
        list[dict]: One dict per medicine with keys:
                    med_name, company, qty_in_stock,
                    tab_price, strip_price, tabs_per_strip
    """
    medicines = []

    try:
        with open(DB_FILENAME, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue  # skip blank lines

                parts = line.split(",")

                if len(parts) != 6:
                    print(
                        f"Warning: Line {line_num} skipped (expected 6 columns, got {len(parts)})"
                    )
                    continue

                try:
                    medicine = {
                        "med_name": parts[0].strip(),
                        "company": parts[1].strip(),
                        "qty_in_stock": int(parts[2].strip()),
                        "tab_price": int(parts[3].strip()),
                        "strip_price": int(parts[4].strip()),
                        "tabs_per_strip": int(parts[5].strip()),
                    }
                    medicines.append(medicine)

                except ValueError as e:
                    print(
                        f"Warning: Line {line_num} skipped — could not parse numbers ({e})"
                    )
                    continue

    except FileNotFoundError:
        print("Warning: medicines.txt not found. Starting with empty inventory.")

    return medicines


def save_all_medicines(med_list):
    """
    Overwrite medicines.txt with the current in-memory inventory.

    Args:
        med_list (list[dict]): The full inventory list to save.
    """
    with open(DB_FILENAME, "w") as f:
        for item in med_list:
            # BUG WAS HERE: was using medicine_name/brand_name/stock/etc. (wrong keys)
            f.write(
                f"{item['med_name']}, "
                f"{item['company']}, "
                f"{item['qty_in_stock']}, "
                f"{item['tab_price']}, "
                f"{item['strip_price']}, "
                f"{item['tabs_per_strip']}\n"
            )


def show_inventory(medicines):
    """
    Print the medicine inventory as a numbered table.
    The ID shown here is what the user types to select a medicine.

    Args:
        medicines (list[dict]): Current inventory list.
    """
    if not medicines:
        print("  No medicines in inventory.")
        return

    # BUG WAS HERE: no ID column — users couldn't know what number to type
    print("=" * 105)
    print(
        "ID".ljust(5),
        "Medicine".ljust(25),
        "Brand".ljust(22),
        "Stock(tabs)".ljust(13),
        "Rate/Tab".ljust(12),
        "Rate/Strip".ljust(13),
        "Tabs/Strip",
    )
    print("=" * 105)

    for i, m in enumerate(medicines, start=1):
        print(
            str(i).ljust(5),
            m["med_name"].ljust(25),
            m["company"].ljust(22),
            str(m["qty_in_stock"]).ljust(13),
            str(m["tab_price"]).ljust(12),
            str(m["strip_price"]).ljust(13),
            str(m["tabs_per_strip"]),
        )
        print("-" * 105)


def ask_for_number(msg, min_value=0):
    """
    Keep prompting until the user enters a valid integer >= min_value.

    Args:
        msg       (str): Prompt shown to the user.
        min_value (int): Minimum acceptable value.

    Returns:
        int: The validated integer.
    """
    while True:
        user_input = input(msg).strip()
        try:
            num = int(user_input)
            if num < min_value:
                print(f"  Error: Number cannot be less than {min_value}.")
            else:
                return num
        except ValueError:
            print("  Error: Please enter a whole number, not text.")
