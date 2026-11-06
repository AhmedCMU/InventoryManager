"""CPS 310 - Homework 1: Inventory Manager
Instructor solution checkpoint.
"""

INVENTORY_FILE = "inventory.txt"
LOW_STOCK_THRESHOLD = 5


def display_menu():
    """Display the main Inventory Manager menu."""
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


def load_inventory(filename):
    """Load inventory records from a pipe-delimited text file."""
    inventory = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                name, category, quantity = line.split("|")
                inventory.append(
                    {
                        "name": name,
                        "category": category,
                        "quantity": int(quantity),
                    }
                )
    except FileNotFoundError:
        return []

    return inventory


def save_inventory(inventory, filename):
    """Save the complete inventory to a pipe-delimited text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in inventory:
            file.write(
                f'{item["name"]}|{item["category"]}|{item["quantity"]}\n'
            )


def view_inventory(inventory):
    """Display all inventory items in a numbered list."""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory:")
    for index, item in enumerate(inventory, start=1):
        print(
            f'{index}. {item["name"]} | {item["category"]} | '
            f'Quantity: {item["quantity"]}'
        )

def validate_new_item(inventory, name, category, quantity):
    """Validate information for a new inventory item."""
    name = name.strip()
    category = category.strip()

    if not name or "|" in name:
        return False

    if not category or "|" in category:
        return False

    if not isinstance(quantity, int) or quantity < 0:
        return False

    for item in inventory:
        if item["name"].lower() == name.lower():
            return False

    return True

def add_item(inventory):
    """Prompt for and add one validated inventory item, then save it."""
    name = input("Enter the item name: ").strip()
    category = input("Enter the category: ").strip()

    quantity_text = input("Enter the quantity: ").strip()

    if not quantity_text.isdigit():
        print("Quantity must be a nonnegative whole number.")
        return

    quantity = int(quantity_text)

    if not validate_new_item(inventory, name, category, quantity):
        print("Invalid item information or item already exists.")
        return

    inventory.append({
        "name": name,
        "category": category,
        "quantity": quantity
    })

    save_inventory(inventory, INVENTORY_FILE)
    print("Item added successfully.")

def update_item_quantity(inventory, item_number, new_quantity):
    """Update an item's quantity using its displayed item number."""
    if item_number < 1 or item_number > len(inventory):
        return False

    if not isinstance(new_quantity, int) or new_quantity < 0:
        return False

    item = inventory[item_number - 1]
    item["quantity"] = new_quantity
    return True

def update_quantity(inventory):
    """Prompt for an item number and replace its quantity, then save it."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)
    selection_text = input("Enter the item number to update: ").strip()

    if not selection_text.isdigit():
        print("Item number must be a valid whole number.")
        return

    selection = int(selection_text)

    quantity_text = input("Enter the new quantity: ").strip()

    if not quantity_text.isdigit():
        print("Quantity must be a nonnegative whole number.")
        return

    quantity = int(quantity_text)

    if not update_item_quantity(inventory, selection, quantity):
        print("Item number is outside the available range.")
        return

def remove_item_by_number(inventory, item_number):
    """Remove an item using its displayed item number."""
    if item_number < 1 or item_number > len(inventory):
        return None

    return inventory.pop(item_number - 1)

def remove_item(inventory):
    """Prompt for an item number, remove that item, then save the inventory."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)
    selection_text = input("Enter the item number to remove: ").strip()

    if not selection_text.isdigit():
        print("Item number must be a valid whole number.")
        return

    selection = int(selection_text)
    removed_item = remove_item_by_number(inventory, selection)

    if removed_item is None:
        print("Item number is outside the available range.")
        return


def find_matching_items(inventory, search_term):
    """Return inventory items whose names match the search term."""
    if not search_term.strip():
        return []

    matches = []

    for item in inventory:
        if search_term.lower() in item["name"].lower():
            matches.append(item)

    return matches

def search_inventory(inventory):
    """Prompt for an item-name search term and display matching items."""
    search_term = input("Enter part or all of an item name: ").strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = find_matching_items(inventory, search_term)

    if not matches:
        print("No inventory items matched your search.")
        return

    print("\nSearch Results:")
    for index, item in enumerate(matches, start=1):
        print(
            f'{index}. {item["name"]} | {item["category"]} | '
            f'Quantity: {item["quantity"]}'
        )

def calculate_summary(inventory):
    """Calculate inventory summary information and return it."""
    unique_items = len(inventory)
    total_quantity = 0
    low_stock_items = 0
    category_counts = {}
    category_labels = {}

    for item in inventory:
        total_quantity += item["quantity"]

        if item["quantity"] < LOW_STOCK_THRESHOLD:
            low_stock_items += 1

        category_key = item["category"].lower()

        if category_key not in category_counts:
            category_counts[category_key] = 0
            category_labels[category_key] = item["category"]

        category_counts[category_key] += 1

    return {
        "unique_items": unique_items,
        "total_quantity": total_quantity,
        "low_stock_items": low_stock_items,
        "category_counts": category_counts,
        "category_labels": category_labels,
    }

def display_summary(inventory):
    """Calculate and display inventory summary information."""
    summary = calculate_summary(inventory)

    print("\nInventory Summary")
    print(f'Unique items: {summary["unique_items"]}')
    print(f'Total quantity: {summary["total_quantity"]}')
    print(f'Low-stock items: {summary["low_stock_items"]}')
    print("\nItems by category:")

    if not summary["category_counts"]:
        print("No categories found.")
        return

    for category_key, count in summary["category_counts"].items():
        category_name = summary["category_labels"][category_key]
        print(f"{category_name}: {count}")

def main():
    """Run the Inventory Manager menu loop."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()

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
            print("Goodbye!")
            break
        else:
            print("Please enter a menu option from 1 through 7.")


if __name__ == "__main__":
    main()
