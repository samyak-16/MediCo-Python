from operations import display_medicines
from read import read_medicines


def main():
    # Extracting medicines :
    medicines = read_medicines()
    # Printing in readable format on the terminal:
    display_medicines(medicines=medicines)


main()
