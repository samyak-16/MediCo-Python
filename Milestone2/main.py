"""
main.py
-----------
Entry point for the MedStore Pvt. Ltd. Wholesale Management System.
Displays the main menu and routes to sale or restock operations.
"""

from inventory import load_stock, display_stock
from selling import run_sale
from buying import run_restock


MENU_OPTIONS = {
    "1": "Browse Available Stock",
    "2": "Process a Customer Sale",
    "3": "Record a Supplier Restock",
    "4": "Exit Application",
}


def print_menu():
    """Print the main navigation menu to the terminal."""
    print("\n╔══════════════════════════════════════╗")
    print("║    MedStore Pvt. Ltd.                ║")
    print("║    Wholesale Management System       ║")
    print("╚══════════════════════════════════════╝")
    print()
    for key, label in MENU_OPTIONS.items():
        print(f"   [{key}]  {label}")
    print()


def run_app():
    """
    Launch the main application loop.

    Loads inventory once at startup (mutations persist in memory).
    Keeps running until the user explicitly chooses to exit.
    """
    try:
        stock = load_stock()
    except Exception as err:
        print(f"  Fatal: Could not load inventory — {err}")
        return

    active = True
    while active:
        print_menu()
        pick = input("  Your choice: ").strip()

        if pick == "1":
            display_stock(stock)

        elif pick == "2":
            print("\n  ── Starting New Sale ──")
            run_sale(stock)

        elif pick == "3":
            print("\n  ── Recording Supplier Restock ──")
            run_restock(stock)

        elif pick == "4":
            print("\n  Goodbye! Closing MedStore system.\n")
            active = False

        else:
            print("  ✗  Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_app()
