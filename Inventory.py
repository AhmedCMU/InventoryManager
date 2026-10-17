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
    
def search_inventory(inventory):
    """Search for inventory items by partial, case-insensitive name."""
    search_term = input("Enter an item name to search for: ").strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = []

    for item in inventory:
        if search_term.casefold() in item["name"].casefold():
            matches.append(item)

    if not matches:
        print("No inventory items matched your search.")
        return

    print("\nSearch results:")

    for number, item in enumerate(matches, start=1):
        print(
            f"{number}. {item['name']} | "
            f"{item['category']} | "
            f"Quantity: {item['quantity']}"
        )
def display_summary(inventory):
    """Display inventory totals and counts by category."""
    total_items = len(inventory)
    total_quantity = 0
    low_stock_items = 0
    category_counts = {}

    for item in inventory:
        total_quantity += item["quantity"]

        if item["quantity"] < 5:
            low_stock_items += 1

        category = item["category"]

        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    print("\nInventory Summary")
    print(f"Unique inventory items: {total_items}")
    print(f"Total quantity: {total_quantity}")
    print(f"Low-stock items: {low_stock_items}")

    print("Items in each category:")

    if not category_counts:
        print("No categories found.")
    else:
        for category, count in category_counts.items():
             print(f"{category}: {count}")    
def display_menu():
    """Display the Inventory Manager main menu."""
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit") 
    
def main():
    """Run the Inventory Manager until the user chooses to exit."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            view_inventory(inventory)

        elif choice == "2":
            add_item(inventory)

        elif choice == "3":
            update_quantity(inventory)

        elif choice == "4":
            remove_item(inventory)

        elif choice == "5":
            search_inventory(inventory)

        elif choice == "6":
            display_summary(inventory)

        elif choice == "7":
            print("Thank you for using Inventory Manager. Goodbye!")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    main()