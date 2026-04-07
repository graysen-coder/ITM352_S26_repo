#Read in a file from a url and save a local csv file with the first 10 rows

import time
import pandas as pd
import numpy as np
import pyarrow

pd.set_option('display.max_columns', None)  # Show all columns in the output

def load_csv(filepath):
    print(f"Loading data from: {filepath}")
    start_time = time.time()

    try:
        df = pd.read_csv(filename, engine='python')
        end_time = time.time()
        load_time = end_time - start_time
        print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print(f"Missing ")

        required_columns = ['quantity', 'unit_price', 'order_date']
        missing_columns = [col for col in required_columns if col not in df.columns]

        #Check if required columns are present

        return df

    except Exception as e:
        print(f"Error occurred while loading the CSV file: {e}")
        return None
    
#Call load csv 

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"
#filename = "sales_data_test.csv"
sales_data = load_csv(filename)

def display_initial_rows(dataframe):
    print("Enter rows to display: ")
    print(f"  Enter a number 1 to {len(dataframe)} to display that many rows")
    print("- Enter 'all' to display all rows")
    print("- to skip preview, press Enter")
    user_input = input("Your choice: ").strip().lower()

    if user_input == '':
        print("Skipping preview.")
    elif user_input == 'all':
        print(dataframe)
    elif user_input.isdigit() and 1 <= int(user_input) <= len(dataframe):
        print(f"Displaying first {user_input} rows:")
        print(dataframe.head(int(user_input)))

def show_employees_by_region(dataframe):
    return

def exit_program():
    return

def display_menu(dataframe):
    menu_options = (
        ("Show the first 10 rows of the data", display_initial_rows),
        ("Show the number of employees by region", show_employees_by_region),
        ("Exit", exit_program)
    )

    print("Available options:")
    for i, (description, _) in enumerate(menu_options, start=1):
        print(f"{i}. {description}")

    try:
        menu_len = len(menu_options)
        choice = int(input(f"Select an option (1-{menu_len}): "))
        if 1 <= choice <= menu_len:
            action = menu_options[choice - 1][1]
            action(dataframe)
        else:
            print("Invalid choice. Please select a valid option.")
    
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the menu options.")

def main():
    while True:
        print("Sales Data Dashboard")
        display_menu(sales_data)


if __name__ == "__main__":
    main()