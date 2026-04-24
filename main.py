#   Task 1 : Open the file medicines.txt which has data in this format and read it :


#  1st  column  shows  the  medicine  name,
#  2nd  column  shows  the  brand  name,
#  3rd column shows the quantity available in stock (in tablets),
#  4th column shows the rate per tablet in rupees,
#  5th  column shows the rate per strip in rupees,
#  and 6th  column shows the number of tablets in one strip.

medicines = []
with open("medicines.txt", "r") as f:
    for line in f:
        medicine_info_by_parts = line.strip().split(",")
        # print(medicine_info_by_parts)
        medicine = {
            "medicine_name": medicine_info_by_parts[0].strip(),
            "brand_name": medicine_info_by_parts[1].strip(),
            "stock": int(medicine_info_by_parts[2]),
            "rate_tablet": int(medicine_info_by_parts[3]),
            "rate_strip": int(medicine_info_by_parts[4]),
            "tablets_per_strip": int(medicine_info_by_parts[5]),
        }
        medicines.append(medicine)
# print(medicines)

# Printing in readable format on the terminal:

for m in medicines:
    print("=" * 50)
    print()
    print("Medicine:", m["medicine_name"])
    print("Brand:", m["brand_name"])
    print("Stock:", m["stock"], "tablets")
    print("Rate per tablet:", m["rate_tablet"], "Rs")
    print("Rate per strip:", m["rate_strip"], "Rs")
    print("Tablets per strip:", m["tablets_per_strip"])
    print()
