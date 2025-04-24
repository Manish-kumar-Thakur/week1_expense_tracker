import csv
import os
from tabulate import tabulate  

user_name = input("Plese enter your Name: ")
print(f"***WELCOME TO EXPENSE TRACKER {user_name.upper()}***")

categories = {
    "food": [],
    "transport": [],
    "entertainment": [],
    "miscellaneous": []
}
FILE_NAME = "transaction.csv"
spent_so_far = 0
total_budget = 0  # Will be set by user


# Define the ExpendableItem class
class ExpendableItem:
    def __init__(self, name, qty, price, note=""):
        self.name = name
        self.qty = qty
        self.price = price
        self.note = note

    def total_cost(self):
        return self.qty * self.price


def choose_category():
    print("\nSelect a category:")
    for i, category in enumerate(categories.keys(), start=1):
        print(f"{i}. {category.capitalize()}")

    while True:
        choice = input("Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return list(categories.keys())[int(choice) - 1]
        print("Invalid choice. Please try again.")


def add_expense():
    global spent_so_far, total_budget
    category = choose_category()
    name = input("Enter item name: ").strip()

    try:
        qty = int(input("Enter quantity: "))
        price = float(input("Enter price per item (NPR): "))
    except ValueError:
        print("Invalid input. Please enter valid numbers for quantity and price.")
        return

    note = input("Enter any note (optional): ")
    item = ExpendableItem(name, qty, price, note)
    cost = item.total_cost()

    if spent_so_far + cost > total_budget:
        print("Warning: This expense exceeds your current budget.")
        print(f"Current Balance: NPR{total_budget - spent_so_far:.2f}")
        print(f"Expense Cost: NPR{cost:.2f}")
        
        choice = input("Do you want to add more budget to proceed? (yes/no): ").strip().lower()
        if choice == "yes":
            while True:
                try:
                    extra = float(input("Enter the amount to add to your budget: NPR "))
                    if extra <= 0:
                        print("Please enter a positive amount.")
                        continue
                    total_budget += extra
                    print(f"Budget upgraded successfully. New total budget: NPR{total_budget:.2f}")
                    break
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
        else:
            print(" Expense not added. Returning to main menu.")
            return

        if spent_so_far + cost > total_budget:
            print(" Even after adding budget, the expense still exceeds your total budget. Cannot proceed.")
            return

    categories[category].append(item)
    spent_so_far += cost
    save_to_csv(category, item)

    print(f"Added {name} to {category}.")
    print(f"Total spent so far: NPR{spent_so_far:.2f}")
    print(f"Remaining budget: NPR{total_budget - spent_so_far:.2f}")


def view_history():
    print("\nTransaction History:")
    table = []
    for category, items in categories.items():
        for item in items:
            table.append([
                category.capitalize(),
                item.name,
                item.qty,
                f"NPR{item.price:.2f}",
                f"NPR{item.total_cost():.2f}",
                item.note
            ])
    if table:
        headers = ["Category", "Item", "Quantity", "Price", "Total", "Note"]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No transactions recorded yet.")


def view_summary():
    print("\nBudget Summary:")
    for category, items in categories.items():
        total = sum(item.total_cost() for item in items)
        if total > 0:
            print(f"{category.capitalize()}: NPR{total:.2f}")
    print(f"\nTotal Spent: NPR{spent_so_far:.2f}")
    print(f"Remaining Balance: NPR{total_budget - spent_so_far:.2f}")


def save_to_csv(category, item):
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, "a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Category", "Name", "Quantity", "Price", "Total", "Note"])
        writer.writerow([category, item.name, item.qty, item.price, item.total_cost(), item.note])


# Main program loop
if __name__ == "__main__":
    while True:
        try:
            total_budget = float(input("Set your initial total budget (NPR): "))
            if total_budget <= 0:
                print("Please enter a positive budget.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View History")
        print("3. View Budget Summary")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_history()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            print("Goodbye! Stay on budget!")
            break
        else:
            print("Invalid option. Please choose again.")
