# Chala Ahmed 

INVENTORY_FILE = "inventory.txt" 

def load_inventory(filename):
    # load inventory item from the file 
    inventory = []

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if line:
                    name, category, quantity = line.split("|")

                    item = {
                        "name": name,
                        "category": category,
                        "quantity": int(quantity)
                    }

                    inventory.append(item)

    except FileNotFoundError:
        print("Inventory file not found. Starting with an empty inventory.")

    return inventory
  

