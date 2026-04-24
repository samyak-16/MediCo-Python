# Different operations (helper function) for the project


def display_medicines(medicines):
    #  medicines is a list of medicine as a dict
    print("=" * 95)
    print(
        "Medicine".ljust(25),
        "Brand".ljust(20),
        "Stock".ljust(10),
        "Rate/Tab".ljust(12),
        "Rate/Strip".ljust(12),
        "Tabs/Strip",
    )
    print("=" * 95)

    for m in medicines:
        print(
            m["medicine_name"].ljust(25),
            m["brand_name"].ljust(20),
            str(m["stock"]).ljust(10),
            str(m["rate_tablet"]).ljust(12),
            str(m["rate_strip"]).ljust(12),
            str(m["tablets_per_strip"]),
        )
        print("-" * 95)
