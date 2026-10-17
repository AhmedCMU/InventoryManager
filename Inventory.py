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
  
def save_inventory(inventory, filename): 
    # save all the inventory item to the file 
    with open(filename, "w") as file:
        for item in inventory:
            line = (
                item["name"] + "|"
                + item["category"] + "|"
                + str(item["quantity"]) + "\n"
            )
            file.write(line)
            
def view_inventory(inventory):
    """Display all inventory items in a numbered list."""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory:")

    for number, item in enumerate(inventory, start=1):
        print(
            f"{number}. {item['name']} | "
            f"{item['category']} | "
            f"Quantity: {item['quantity']}"
        )
def add_item(inventory):
    """Ask for item details, validate them, and add a new item."""
    name = input("Enter the item name: ").strip()

    if not name:
        print("Item name cannot be empty.")
        return

    if "|" in name:
        print("Item name cannot contain '|'.")
        return

    for item in inventory:
        if item["name"].casefold() == name.casefold():
            print("An item with this name already exists.")
            return

    category = input("Enter the category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    if "|" in category:
        print("Category cannot contain '|'.")
        return

    quantity_text = input("Enter the quantity: ").strip()

    try:
        quantity = int(quantity_text)
    except ValueError:
        print("Quantity must be a nonnegative whole number.")
        return

    if quantity < 0:
        print("Quantity must be a nonnegative whole number.")
        return

    item = {
        "name": name,
        "category": category,
        "quantity": quantity
    }

    inventory.append(item)
    save_inventory(inventory, INVENTORY_FILE)

    print("Item added successfully.")


