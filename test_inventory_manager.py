import pytest

from inventory_manager import (
    load_inventory,
    save_inventory,
    find_matching_items,
    remove_item_by_number,
    update_item_quantity,
    calculate_summary,
    validate_new_item,
    add_item, 
    main, 
)

@pytest.fixture
def sample_inventory():
    return [
        {"name": "Laptop", "category": "Electronics", "quantity": 10},
        {"name": "Wireless Mouse", "category": "Accessories", "quantity": 3},
        {"name": "Wireless Keyboard", "category": "Accessories", "quantity": 5},
        {"name": "Monitor", "category": "Electronics", "quantity": 8},
    ]

def test_load_inventory_reads_valid_file(tmp_path):
    test_file = tmp_path / "inventory.txt"
    test_file.write_text(
        "Laptop|Electronics|10\nMouse|Accessories|3\n",
        encoding="utf-8"
    )

    result = load_inventory(test_file)

    assert len(result) == 2
    assert result[0]["name"] == "Laptop"
    assert result[1]["name"] == "Mouse"


def test_load_inventory_converts_quantity_to_integer(tmp_path):
    test_file = tmp_path / "inventory.txt"
    test_file.write_text("Laptop|Electronics|10\n", encoding="utf-8")

    result = load_inventory(test_file)

    assert result[0]["quantity"] == 10
    assert isinstance(result[0]["quantity"], int)


def test_load_inventory_ignores_blank_lines(tmp_path):
    test_file = tmp_path / "inventory.txt"
    test_file.write_text(
        "Laptop|Electronics|10\n\nMouse|Accessories|3\n",
        encoding="utf-8"
    )

    result = load_inventory(test_file)

    assert len(result) == 2


def test_load_inventory_missing_file_returns_empty_list(tmp_path):
    test_file = tmp_path / "missing.txt"

    result = load_inventory(test_file)

    assert result == []   

def test_save_inventory_writes_items(tmp_path):
    test_file = tmp_path / "inventory.txt"

    inventory = [
        {"name": "Laptop", "category": "Electronics", "quantity": 10},
        {"name": "Mouse", "category": "Accessories", "quantity": 3},
    ]

    save_inventory(inventory, test_file)

    content = test_file.read_text(encoding="utf-8")

    assert content == (
        "Laptop|Electronics|10\n"
        "Mouse|Accessories|3\n"
    )


def test_save_inventory_empty_list(tmp_path):
    test_file = tmp_path / "inventory.txt"

    save_inventory([], test_file)

    assert test_file.read_text(encoding="utf-8") == "" 
    
def test_save_and_load_inventory_round_trip(tmp_path):
    # Arrange
    test_file = tmp_path / "inventory.txt"

    inventory = [
        {"name": "Laptop", "category": "Electronics", "quantity": 10},
        {"name": "Mouse", "category": "Accessories", "quantity": 3},
        {"name": "Keyboard", "category": "Accessories", "quantity": 5},
    ]

    # Act
    save_inventory(inventory, test_file)
    loaded_inventory = load_inventory(test_file)

    # Assert
    assert loaded_inventory == inventory
    
def test_search_finds_exact_item_name(sample_inventory):
    # Arrange
    search_term = "Laptop"

    # Act
    result = find_matching_items(sample_inventory, search_term)

    # Assert
    assert len(result) == 1
    assert result[0]["name"] == "Laptop"


def test_search_finds_partial_item_name(sample_inventory):
    # Arrange
    search_term = "top"

    # Act
    result = find_matching_items(sample_inventory, search_term)

    # Assert
    
def test_search_ignores_capitalization(sample_inventory):
    # Arrange
    search_term = "LAPTOP"

    # Act
    result = find_matching_items(sample_inventory, search_term)

    # Assert
    assert len(result) == 1
    assert result[0]["name"] == "Laptop"


def test_search_returns_multiple_matching_items(sample_inventory):
    # Arrange
    search_term = "Wireless"

    # Act
    result = find_matching_items(sample_inventory, search_term)

    # Assert
    assert len(result) == 2
    assert result[0]["name"] == "Wireless Mouse"
    assert result[1]["name"] == "Wireless Keyboard"


def test_search_returns_empty_list_when_no_match(sample_inventory):
    # Arrange
    search_term = "Printer"

    # Act
    result = find_matching_items(sample_inventory, search_term)

    # Assert
    assert result == []


def test_search_returns_empty_list_for_whitespace_search(sample_inventory):
    # Arrange
    search_term = "   "

    # Act
    result = find_matching_items(sample_inventory, search_term)

    # Assert
    assert result == [] 
    
def test_remove_first_item(sample_inventory):
    # Arrange
    inventory = sample_inventory.copy()

    # Act
    removed = remove_item_by_number(inventory, 1)

    # Assert
    assert removed["name"] == "Laptop"
    assert [item["name"] for item in inventory] == [
        "Wireless Mouse", "Wireless Keyboard", "Monitor"
    ]


def test_remove_middle_item(sample_inventory):
    # Arrange
    inventory = sample_inventory.copy()

    # Act
    removed = remove_item_by_number(inventory, 2)

    # Assert
    assert removed["name"] == "Wireless Mouse"
    assert [item["name"] for item in inventory] == [
        "Laptop", "Wireless Keyboard", "Monitor"
    ]


def test_remove_last_item(sample_inventory):
    # Arrange
    inventory = sample_inventory.copy()

    # Act
    removed = remove_item_by_number(inventory, 4)

    # Assert
    assert removed["name"] == "Monitor"
    assert [item["name"] for item in inventory] == [
        "Laptop", "Wireless Mouse", "Wireless Keyboard"
    ]


import pytest

@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero", "negative-number", "above-inventory-length"]
)
def test_remove_rejects_invalid_item_numbers(sample_inventory, item_number):
    # Arrange
    inventory = sample_inventory.copy()
    original_inventory = inventory.copy()

    # Act
    result = remove_item_by_number(inventory, item_number)

    # Assert
    assert result is None
    assert inventory == original_inventory 
    
@pytest.mark.parametrize(
    "new_quantity",
    [0, 12],
    ids=["zero-quantity", "positive-quantity"]
)
def test_update_item_quantity_accepts_valid_quantity(
    sample_inventory, new_quantity
):
    # Arrange
    inventory = [item.copy() for item in sample_inventory]
    original_items = [item.copy() for item in inventory]

    # Act
    result = update_item_quantity(inventory, 2, new_quantity)

    # Assert
    assert result is True
    assert inventory[1]["quantity"] == new_quantity

    # Verify unrelated items remain unchanged
    assert inventory[0] == original_items[0]
    assert inventory[2:] == original_items[2:]


@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero", "negative-number", "above-inventory-length"]
)
def test_update_rejects_invalid_item_numbers(
    sample_inventory, item_number
):
    # Arrange
    inventory = [item.copy() for item in sample_inventory]
    original_inventory = [item.copy() for item in inventory]

    # Act
    result = update_item_quantity(inventory, item_number, 10)

    # Assert
    assert result is False
    assert inventory == original_inventory


def test_update_rejects_negative_quantity(sample_inventory):
    # Arrange
    inventory = [item.copy() for item in sample_inventory]
    original_inventory = [item.copy() for item in inventory]

    # Act
    result = update_item_quantity(inventory, 2, -5)

    # Assert
    assert result is False
    assert inventory == original_inventory


def test_update_rejects_nonnumeric_quantity(sample_inventory):
    # Arrange
    inventory = [item.copy() for item in sample_inventory]
    original_inventory = [item.copy() for item in inventory]

    # Act
    result = update_item_quantity(inventory, 2, "abc")

    # Assert
    assert result is False
    assert inventory == original_inventory

def test_validate_accepts_valid_new_item(sample_inventory):
    assert validate_new_item(
        sample_inventory, "Tablet", "Electronics", 6
    ) is True


@pytest.mark.parametrize(
    "name, category, quantity",
    [
        ("", "Electronics", 5),
        ("Laptop", "", 5),
        ("New|Laptop", "Electronics", 5),
        ("Tablet", "Elect|ronics", 5),
        ("Tablet", "Electronics", -1),
        ("Laptop", "Electronics", 5),
        ("laptop", "Electronics", 5),
    ],
    ids=[
        "empty-name",
        "empty-category",
        "pipe-in-name",
        "pipe-in-category",
        "negative-quantity",
        "duplicate-name",
        "duplicate-name-different-capitalization",
    ],
)
def test_validate_rejects_invalid_new_item(
    sample_inventory, name, category, quantity
):
    assert validate_new_item(
        sample_inventory, name, category, quantity
    ) is False

def test_summary_counts_unique_items(sample_inventory):
    summary = calculate_summary(sample_inventory)

    assert summary["unique_items"] == 4


def test_summary_calculates_total_quantity(sample_inventory):
    summary = calculate_summary(sample_inventory)

    assert summary["total_quantity"] == 26


def test_summary_counts_low_stock_items(sample_inventory):
    summary = calculate_summary(sample_inventory)

    assert summary["low_stock_items"] == 1


def test_summary_counts_items_by_category(sample_inventory):
    summary = calculate_summary(sample_inventory)

    assert summary["category_counts"] == {
        "electronics": 2,
        "accessories": 2,
    }


def test_summary_ignores_category_capitalization():
    inventory = [
        {"name": "Laptop", "category": "Electronics", "quantity": 10},
        {"name": "Mouse", "category": "electronics", "quantity": 3},
    ]

    summary = calculate_summary(inventory)

    assert summary["category_counts"] == {"electronics": 2}


def test_summary_empty_inventory():
    summary = calculate_summary([])

    assert summary["unique_items"] == 0
    assert summary["total_quantity"] == 0
    assert summary["low_stock_items"] == 0
    assert summary["category_counts"] == {}
    assert summary["category_labels"] == {}


@pytest.mark.parametrize(
    "quantity, expected_low_stock",
    [
        (4, 1),
        (5, 0),
    ],
    ids=["below-threshold", "at-threshold"],
)
def test_summary_low_stock_threshold(quantity, expected_low_stock):
    inventory = [
        {"name": "Keyboard", "category": "Accessories", "quantity": quantity}
    ]

    summary = calculate_summary(inventory)

    assert summary["low_stock_items"] == expected_low_stock
    
def test_add_item_success(monkeypatch, tmp_path):
    import inventory_manager

    inventory = []

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: {
            "Enter the item name: ": "Tablet",
            "Enter the category: ": "Electronics",
            "Enter the quantity: ": "6"
        }[prompt]
    )

    monkeypatch.setattr(
        inventory_manager,
        "INVENTORY_FILE",
        str(tmp_path / "inventory.txt")
    )

    add_item(inventory)

    assert inventory == [
        {"name": "Tablet", "category": "Electronics", "quantity": 6}
    ]
    assert (tmp_path / "inventory.txt").exists()

    inventory = []

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: {
            "Enter the item name: ": "Tablet",
            "Enter the category: ": "Electronics",
            "Enter the quantity: ": "6"
        }[prompt]
    )

    monkeypatch.setattr(
        inventory_manager,
        "INVENTORY_FILE",
        str(tmp_path / "inventory.txt")
    )

    add_item(inventory)

    assert inventory == [
        {"name": "Tablet", "category": "Electronics", "quantity": 6}
    ]
    assert (tmp_path / "inventory.txt").exists() 
    
def test_main_exits_when_user_selects_seven(monkeypatch, capsys, tmp_path):
    import inventory_manager

    monkeypatch.setattr(
        inventory_manager,
        "INVENTORY_FILE",
        str(tmp_path / "inventory.txt")
    )

    monkeypatch.setattr("builtins.input", lambda prompt: "7")

    main()

    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out