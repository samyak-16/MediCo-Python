from inventory import show_inventory, ask_for_number, save_all_medicines
from invoice import create_bill_receipt


def process_customer_sale(inventory_list):
    # It asks us who is buying aka the customer's name.
    buyer_name = input("What is the buyer's name?")

    # It makes sure we didn't just press enter without the name.
    while buyer_name.strip() == "":
        print("Please provide a valid customer name.")
        buyer_name = input("What is the buyer's name?")

    shopping_cart = []
    total_to_pay = 0

    buying_more = True
    while buying_more:
        # It shows what we have in the stock.
        show_inventory(inventory_list)

        chosen_id = ask_for_number(
            "Enter the ID of the medicine to sell or 0 to stop: ", 0
        )

        if chosen_id == 0:
            break

        if chosen_id > len(inventory_list):
            print("We don't have that ID. Table ma herna hau.")
            continue

        # This code gets the medicine from our stock which are listed by the customers.
        selected_med = inventory_list[chosen_id - 1]
        print(f"\nYou selected: {selected_med['med_name']} ({selected_med['company']})")

        print("How are you selling this?")
        print(" 1 -> By Tablet")
        print(" 2 -> By Strip")

        sale_mode = ask_for_number("Your choice (1 or 2): ", 1)

        # This here forces the customer to choose between tablet and strip as 1 and 2.
        while sale_mode not in [1, 2]:
            print("Please pick either 1 or 2.")
            sale_mode = ask_for_number("Your choice (1 or 2): ", 1)

        how_many = ask_for_number("How many do they want? ", 1)

        money_saved = 0
        final_cost = 0

        if sale_mode == 1:
            # Here is the code for selling the tablet individually, if we are low in stock.
            if how_many > selected_med["qty_in_stock"]:
                print(
                    f"Sorry, we only have {selected_med['qty_in_stock']} tablets left."
                )
                continue

            final_cost = how_many * selected_med["tab_price"]
            unit_label = "Tablets"
            selected_med["qty_in_stock"] -= how_many

        elif sale_mode == 2:
            # Here is the code for selling an entire strip.
            total_tabs_needed = how_many * selected_med["tabs_per_strip"]

            if total_tabs_needed > selected_med["qty_in_stock"]:
                strips_left = (
                    selected_med["qty_in_stock"] // selected_med["tabs_per_strip"]
                )
                print(f"Not enough stock! We only have {strips_left} full strips.")
                continue

            final_cost = how_many * selected_med["strip_price"]
            unit_label = "Strips"

            # Code for getting a 5% discount if they buy 2 or more strips.
            if how_many >= 2:
                money_saved = final_cost * 0.05
                final_cost = final_cost - money_saved
                print(
                    f"** Huhh Awesome! 5% discount applied. Saved Rs. {money_saved} **"
                )

            # Deducts the medicine from our stocks.
            selected_med["qty_in_stock"] -= total_tabs_needed

        # This code records the purchase in the cart.
        shopping_cart.append(
            {
                "item_name": selected_med["med_name"],
                "quantity": how_many,
                "unit_type": unit_label,
                "cost": final_cost,
                "discount_amt": money_saved,
            }
        )

        total_to_pay += final_cost
        print(f"Added to bill! Current total is Rs. {total_to_pay}")

        # This here checks if the customers want any other medicines or not.
        ans = input("\nDo they want to buy something else? (y/n): ")
        if ans.lower() != "y":
            buying_more = False

    # This generates bill and save new stock.
    if len(shopping_cart) > 0:
        create_bill_receipt("sale", buyer_name, shopping_cart, total_to_pay)
        save_all_medicines(inventory_list)
