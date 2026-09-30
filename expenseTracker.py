import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "amount", "description"]


def load_expenses():
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def add_expense():
    expense_date = input("Date (YYYY-MM-DD, blank for today): ").strip()
    if not expense_date:
        expense_date = date.today().isoformat()  # noqa: DTZ011
    else:
        try:
            expense_date = date.fromisoformat(expense_date).isoformat()
        except ValueError:
            print("Please enter a valid date.")
            return

    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    try:
        amount = Decimal(input("Amount: ").strip())
        if not amount.is_finite() or amount <= 0:
            raise InvalidOperation
    except InvalidOperation:
        print("Enter an amount greater than zero.")
        return

    description = input("Description (optional): ").strip()
    write_header = not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "date": expense_date,
                "category": category,
                "amount": f"{amount:.2f}",
                "description": description,
            }
        )
    print("Expense saved.")


def show_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet.")
        return

    print("\nDate        Category             Amount   Description")
    print("-" * 65)
    for expense in expenses:
        print(
            f"{expense['date']:<11} {expense['category']:<20} "
            f"{Decimal(expense['amount']):>8.2f}   {expense['description']}"
        )


def show_summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet.")
        return

    totals = {}
    overall = Decimal("0")
    for expense in expenses:
        amount = Decimal(expense["amount"])
        category = expense["category"]
        totals[category] = totals.get(category, Decimal("0")) + amount
        overall += amount

    print(f"\nTotal spent: {overall:.2f}")
    print("By category:")
    for category, amount in sorted(totals.items()):
        print(f"  {category}: {amount:.2f}")


def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add expense")
        print("2. View expenses")
        print("3. View summary")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
