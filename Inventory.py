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

def update_quantity(inventory):
    """Update the quantity of an existing inventory item."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)

    selection = input("Enter the item number to update: ").strip()

    try:
        item_number = int(selection)
    except ValueError:
        print("Invalid item number.")
        return

    if item_number < 1 or item_number > len(inventory):
        print("Invalid item number.")
        return

    new_quantity_text = input("Enter the new quantity: ").strip()

    try:
        new_quantity = int(new_quantity_text)
    except ValueError:
        print("Quantity must be a nonnegative whole number.")
        return

    if new_quantity < 0:
        print("Quantity must be a nonnegative whole number.")
        return

    item = inventory[item_number - 1]
    item["quantity"] = new_quantity

    save_inventory(inventory, INVENTORY_FILE)

    print(
        f"Updated {item['name']} quantity to {new_quantity}."
    )

#remove item function
def remove_item(inventory):
    """Remove an inventory item selected by its number."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)

    selection = input("Enter the item number to remove: ").strip()

    try:
        item_number = int(selection)
    except ValueError:
        print("Invalid item number.")
        return

    if item_number < 1 or item_number > len(inventory):
        print("Invalid item number.")
        return

    removed_item = inventory.pop(item_number - 1)

    save_inventory(inventory, INVENTORY_FILE)

    print(f"Item removed: {removed_item['name']}")
    
