"""Simple CLI calculator: add, subtract, multiply, divide.

Prompts the user for two numbers and an operation, then prints the result.
Includes input validation and division-by-zero handling.
"""

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please enter a numeric value.")


def choose_operation():
    print("Choose operation:")
    print("1) Add")
    print("2) Subtract")
    print("3) Multiply")
    print("4) Divide")
    while True:
        choice = input("Enter choice (1/2/3/4): ").strip()
        if choice in {"1", "2", "3", "4"}:
            return choice
        print("Invalid choice. Enter 1, 2, 3 or 4.")


def main():
    while True:
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        choice = choose_operation()

        try:
            if choice == "1":
                result = add(a, b)
            elif choice == "2":
                result = subtract(a, b)
            elif choice == "3":
                result = multiply(a, b)
            elif choice == "4":
                result = divide(a, b)
            print(f"Result: {result}")
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed.")

        again = input("Perform another calculation? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()
