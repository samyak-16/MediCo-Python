import datetime


def create_bill_receipt(txn_type, person_or_company, purchased_items, final_total):
    # This here creates a txt file for billing.

    # This here gets the date and time to make unique filename.
    now = datetime.datetime.now()
    time_str = now.strftime("%Y%m%d_%H%M%S")

    # This names the txt file in accordance of the buying or selling.
    file_name = f"{txn_type}_receipt_{time_str}.txt"

    with open(file_name, "w") as bill:
        bill.write("**************************************************\n")
        bill.write("              MedStore Pvt. Ltd.                  \n")
        bill.write("             Wholesale Distributor                \n")
        bill.write("**************************************************\n")

        bill.write(f"Type: {txn_type.upper()}\n")
        bill.write(f"Name: {person_or_company}\n")
        bill.write(f"Date: {now.strftime('%d-%m-%Y %H:%M')}\n")
        bill.write("--------------------------------------------------\n")
        bill.write(f"{'Item Name':<20} {'Qty':<5} {'Type':<10} {'Amount':<10}\n")
        bill.write("--------------------------------------------------\n")

        for p_item in purchased_items:
            bill.write(
                f"{p_item['item_name']:<20} {p_item['quantity']:<5} {p_item['unit_type']:<10} Rs. {p_item['cost']:<10}\n"
            )

            # show discount if any
            if "discount_amt" in p_item and p_item["discount_amt"] > 0:
                bill.write(f"    -> 5% Discount saved: Rs. {p_item['discount_amt']}\n")

        bill.write("--------------------------------------------------\n")
        bill.write(f"GRAND TOTAL:                        Rs. {final_total}\n")
        bill.write("--------------------------------------------------\n")
        bill.write("         Thank you! Have a great day!             \n")
        bill.write("**************************************************\n")

    print(f"\n=> Done! The receipt has been saved as '{file_name}'")
