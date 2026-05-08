# Here is the main Program for MedStore.
from inventory import read_medicines, show_inventory
from selling import process_customer_sale
from buying import handle_supplier_restock


def run_app():
    # Here is the main menu loop of our program.
    print("\n" + "*" * 40)
    print(" Welcome to MedStore Wholesale System ")
    print("*" * 40)

    # It loads the fresh data from text file every time we show the menu.
    meds = read_medicines()

    app_running = True
    while app_running:
        print("\n--- WHAT WOULD YOU LIKE TO DO? ---")
        print(" 1) View all medicines in stock")
        print(" 2) Sell medicine to a customer")
        print(" 3) Buy/Restock from a supplier")
        print(" 4) Quit the program")
        print("----------------------------------")

        user_choice = input("Enter your choice (1-4): ").strip()

        if user_choice == "1":
            show_inventory(meds)

        elif user_choice == "2":
            print("\n>> STARTING A NEW SALE <<")
            process_customer_sale(meds)

        elif user_choice == "3":
            print("\n>> NEW SUPPLIER RESTOCK <<")
            handle_supplier_restock(meds)

        elif user_choice == "4":
            print("\nExiting the app. Thanks for using our Application!")
            app_running = False

        else:
            print("\ncha cha, that's not a valid choice.")


# It runs the code if the file is directly run
if __name__ == "__main__":
    run_app()
