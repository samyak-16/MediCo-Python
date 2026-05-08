from inventory import show_inventory, ask_for_number, save_all_medicines
from invoice import create_bill_receipt


def handle_supplier_restock(inventory_list):
    # It asks us for the supplier's name.
    distributor = input("What's the name of the supplier? ")

    while distributor.strip() == "":
        print("Supplier name is required.")
        distributor = input("What's the name of the supplier? ")

    restock_cart = []
    total_investment = 0

    keep_adding = True
    while keep_adding:
        # This shows what we currently have in stock.
        show_inventory(inventory_list)

        item_id = ask_for_number(
            "Enter the ID of the medicine to restock or type 0 to exit: ", 0
        )

        if item_id == 0:
            break

        if item_id > len(inventory_list):
            print("Cha cha cha! Please choose a number from the list.")
            continue

        # This grabs the selected medicine from our stock.
        med = inventory_list[item_id - 1]
        print(f"\nRestocking: {med['med_name']} (Brand: {med['company']})")

        print("Are you adding tablets or strips?")
        print(" [1] Tablets")
        print(" [2] Strips")

        add_mode = ask_for_number("Choose 1 or 2: ", 1)

        while add_mode not in [1, 2]:
            print("Wrong choice. Type 1 or 2.")
            add_mode = ask_for_number("Choose 1 or 2: ", 1)

        amount_to_add = ask_for_number("How many are you adding? ", 1)

        item_cost = 0

        if add_mode == 1:
            # Here happens the addition of the loose tablets.
            item_cost = amount_to_add * med["tab_price"]
            type_label = "Tabs"
            med["qty_in_stock"] += amount_to_add
        elif add_mode == 2:
            # Here happens the addition of the full strips.
            item_cost = amount_to_add * med["strip_price"]
            type_label = "Strips"
            # This here multiplies strips by tablets per strip to update total tablet stock.
            med["qty_in_stock"] += amount_to_add * med["tabs_per_strip"]

        # This here store info for the receipt.
        restock_cart.append(
            {
                "item_name": med["med_name"],
                "quantity": amount_to_add,
                "unit_type": type_label,
                "cost": item_cost,
            }
        )

        total_investment += item_cost
        print(f"Restocked! Total cost so far: Rs. {total_investment}")

        # This asks us to continue or not.
        reply = input("\nAdd another medicine from supplier? (y/n): ")
        if reply.lower() != "y":
            keep_adding = False

    # This here creates receipt and save file if we bought anything to refill the stock.
    if len(restock_cart) > 0:
        create_bill_receipt("restock", distributor, restock_cart, total_investment)
        save_all_medicines(inventory_list)
