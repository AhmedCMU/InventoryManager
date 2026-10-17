# Inventory Manager Testing

| # | Feature | Input or Action | Expected Result | Actual Result | Pass/Fail |

1, Start with missing file// run with out the right file name// Starts without crashing// Displayed message and menu// PASS

2, View inventory//select option 1// Displays saved items// Five items displayed correctly// PASS

3, Add a valid item //Add USB cable, category Electronic, quantity 6 // Program adds the item and displays a success message// USB cable was added successfully// PASS

4, Enter an empty item name//press enter with out naming // Program rejects the empty name// Program displayed an error message// PASS

5, Add a duplicate item name// enter laptop charger// Program rejects duplicate names ignoring capitalization// The program rejected "laptop charger" because "Laptop Charger" already existed. PASS

6, Enter nonnumeric quantity// enter anbs as quantity// Program rejects text as a quantity// Program displayed a quantity validation error// PASS

7, Enter negative quantity// enter -3 // Program rejects a negative quantity// Program displayed a quantity validation error// PASS

8, Update item quantity//Change USB cable quantity to 15 // Program updates the selected item's quantity// USB cable quantity was updated to 15// PASS

9, Enter an invalid item number//enter 99 as item numbers // Program rejects an item number that does not exist in the list// Program displayed "Invalid item number"// PASS

10, Remove an item //remove USB cable // Program removes the selected item// USB cable was removed successfully// PASS

11, Search using a partial name// typing "charg"// Program finds items matching part of a name, regardless of capitalization// Searching for "charg" found Laptop Charger// PASS

12, Search for a nonexistent item//typing Tablet // Program displays a message when there are no matches// Searching for "Tablet" returned no matches// PASS

13, View inventory summary//select option 6 // Program displays item count, total quantity, low-stock items, and category counts// Displayed 5 items, total quantity 52, 2 low-stock items, and correct category counts// PASS

14, Restart program to check saved data//restart and select 1 // Program reloads the saved inventory correctly// The five expected items appeared after restarting// PASS

15, Enter an invalid menu option// enter 99// Program rejects an option outside 1–7// Entering 9 displayed an error and returned to the menu// PASS

16, Exit the program// enter 7 for exit// Program exits normally when option 7 is selected// Program displayed a goodbye message and returned to the terminal//. PASS
