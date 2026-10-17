# AI Usage Report

## Tools Used

ChatGpt, Google search

## How AI Was Used.

I used AI assistance especially to come up and logic behind the searching function of my project which help me to understand how it work and how we search using the key.

## Example Prompts

Explain how to write a function that updates an inventory item.
help me to come up with function that search item in the invetory regardless of capitalization

## Suggestions Accepted

I accepted suggestions to validate user input before removing an inventory item, handle invalid inputs without crashing the program

## Suggestions Rejected or Modified

[Describe at least one suggestion that was incorrect, unnecessary, incomplete, or changed before use.]

## Verification

I tested every function that AI generated for before I commited. I run code and feed the wrong input to check wheather the funtion crush or not.

[Explain how all AI-assisted code or documentation was tested and verified.]

## Code Understanding

# def search_inventory(inventory):

creating the function that search item in inventory using the user key term. the function search while neglecting lowercase and upercase because the funtion use .casefold in both users key term and inventory list so it does not matter the user upper or lower case. the function only give error message if the user enter the empty search and if nothing is find it inform the user that nothing is match the user search.

# def remove_item(inventory):

creating the remove item funtion. the program first check if the inventory is empty or not if not inventory:
the program ask which item want to remove and also it send the error message if the user type string instade of numbers and also check if the number is with in the valid range or not. after confirm the valid imput it pop the item that the user choose.
