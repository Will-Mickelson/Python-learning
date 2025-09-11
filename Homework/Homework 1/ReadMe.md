Overview
The contact Manager is a command-line program that allows the user to create, store, update, delete, search, and analyze contact records. Each contact is represented as a Python dictionary with clear keys. All contacts are stored together in another dictionary where the keys are unique ID's. 

Key Features: 
Create/Add new contacts
Display a single contact or list all contacts
Search by any field for the contacts
Update/delete contacts
Merge duplicate contacts
Generate stats on the contatcs
Detect duplicate contacts
Export contacts by category
Save and load contacts to/from a JSON file

How to run the Program: 
1: Have Python 3.9+ installed
2: Save the program as contact_manager.py
3: open terminal/command prompt
4: Run the file
5: Choose the option you want from the main menu
6: To exit, type 0 in the menu

Function Documentation with Examples: 
from contact_manager import (
    add_contact, search_contacts_by_name, generate_contact_statistics, find_duplicate_contacts
)

# Initialize an empty DB
db = {}

# Add a new contact
cid = add_contact(db, {
    "first_name": "Alice",
    "last_name": "Nguyen",
    "phone": "402-555-1111",
    "email": "alice@example.com",
    "address": {"street": "", "city": "Omaha", "state": "NE", "zip_code": ""},
    "category": "work",
    "notes": "Met at conference",
    "created_date": "2025-09-03",
    "last_modified": "2025-09-03"
})
print(cid)   # Example output: "contact_001"

# Search by name
results = search_contacts_by_name(db, "alice")
print(results.keys())   # Example output: dict_keys(['contact_001'])

# Generate statistics
stats = generate_contact_statistics(db)
print(stats["total_contacts"])   # Example output: 1

# Find duplicates
dupes = find_duplicate_contacts(db)
print(dupes)   # Example output: {'phone_duplicates': [], 'email_duplicates': [], 'name_duplicates': []}

Limitations: 
User interface is command-line
Minimal input validation

Future Improvements:
Add a GUI
Stronger validation
Integrate with an external database

Sample Usage Scenarios: 
Personal address book
Work contact management