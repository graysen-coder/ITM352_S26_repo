#Assignment 2 - Sales Data Dashboard
#Graysen Oumi
#March 6 2026
#Extra requirements: 1 and 7
#1. For each result, ask the user if they want the results exported to an Excel file (that can be read directly into Excel). Ask the user what filename they want.
#7. Before performing an analysis, ask the user what date range of sales data to use. Use only that range for the analysis. After a lot of troubleshooting, I was unable to get this requirement fulfilled because we were forced to coerce the data to NaT if it is a different format
#There's a lot of data that is not in the correct format and gets converted to NaT which causes the date filtering to not work because all the dates are NaT. 

#Implementing requirement 8 as a substitute for 7

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
        print(f"Columns: {df.columns.tolist()}")
        df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce')  # Convert order_date to datetime, coercing errors to NaT

        #df.fillna(0, inplace=True)  # Fill NaN values with 0 for numeric columns

        df['sales'] = df['quantity'] * df['unit_price']  # Create a new 'sales' column as quantity * unit_price

        required_columns = ['quantity', 'unit_price', 'order_date']

        # Check if required columns are present

        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Warning: Missing required columns: {missing_columns}")        
        else: 
            print("All required columns are present.")

        required_columns = ['quantity', 'unit_price', 'order_date']

        missing_columns = [col for col in required_columns if col not in df.columns]

        #Check if required columns are present

        return df

    except Exception as e:
        print(f"Error occurred while loading the CSV file: {e}")
        return None

#Function to fulfill extra requirement 1, ask user if they want to export the pivot table to an excel file, if yes then ask for filename and save the file
def export_to_csv(pivot_table):
    print("\nWould you like to export the results to an Excel file?")
    print("1. Yes")
    print("2. No")
    export_input = input("Enter your choice: ").strip()

    if export_input == "1":
        filename = input("Enter the filename (without extension): ").strip()
        pivot_table.to_csv(f"{filename}.csv")
        print(f"Pivot table exported to {filename}.csv")

#Function for extra requirement 7, ask user for a date range and filter the dataframe to only include rows within that date range before performing the analysis
#I can't figure out how to get all of the dates into a standardized format that doesn't require coercing to NaT because I would have to assume that there is a 20 in front of years like 19 or 18 so they are 2018
#but dates can be a very varied thing, the data could also technically be from 1920 or 1918 so I would be making a lot of assumptions that might be wrong
def get_date_filtered_dataframe(dataframe):

    dataframe['order_date'] = pd.to_datetime(dataframe['order_date'], format='%m/%d/%Y')

    print(f"\nData available from {dataframe['order_date'].min().date()} to {dataframe['order_date'].max().date()}")
    print("Enter the date range for the analysis (format: MM/DD/YYYY)")
    
    while True:
        start_date = input("Enter the start date: ").strip()
        end_date = input("Enter the end date: ").strip()
        try:
            start_date = pd.to_datetime(start_date, format='%m/%d/%Y')
            end_date = pd.to_datetime(end_date, format='%m/%d/%Y') + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            if start_date > end_date:
                print("Start date must be before end date. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY.")
    
    filtered = dataframe[(dataframe['order_date'] >= start_date) & (dataframe['order_date'] <= end_date)]
    
    print(f"\nFiltering data from {start_date.date()} to {end_date.date()}")
    print(f"Found {len(filtered)} records in this date range.")
    
    if filtered.empty:
        print("No data found for the selected date range.")
        return None
    
    return filtered

#Function for extra requirement 8
#Add an analytic that shows sales by region and product, showing the percentage of the quantity and total sales per region and product. This percentage should be a new column in the pivot table.
def show_sales_by_region_and_product(dataframe):
    dataframe['sales'] = dataframe['quantity'] * dataframe['unit_price']
    
    pivot_table = pd.pivot_table(
        dataframe,
        index=['sales_region', 'product_category'],
        values=['quantity', 'sales'],
        aggfunc='sum'
    )

    pivot_table['quantity_%'] = (pivot_table['quantity'] / pivot_table['quantity'].sum() * 100).round(2)
    pivot_table['sales_%'] = (pivot_table['sales'] / pivot_table['sales'].sum() * 100).round(2)

    print("\nSales by Region and Product:")
    print(pivot_table)
    return



def display_initial_rows(dataframe):
    print("Enter rows to display: ")
    print(f"  Enter a number 1 to {len(dataframe)} to display that many rows")
    print("- Enter 'all' to display all rows")
    print("- to skip preview, press Enter")
    user_input = input("Your choice: ").strip().lower()

    if user_input == '':
        print("Skipping preview.\n")
        return
    
    elif user_input == 'all':
        print(dataframe)
        print("\n")

    elif user_input.isdigit() and 1 <= int(user_input) <= len(dataframe):
        print(f"Displaying first {user_input} rows:")
        print(dataframe.head(int(user_input)))
        print("\n")

    else:
        print("Invalid input. Please try again.")

def show_employees_by_region(dataframe):

    pivot_table = pd.pivot_table(dataframe, values='employee_id', index='sales_region', aggfunc=pd.Series.nunique)
    pivot_table.columns = ['Number of Employees']

    print("\nNumber of employees by region:")
    print(pivot_table)

    export_to_csv(pivot_table)

    return

def show_average_sales_by_region(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index='sales_region', aggfunc=np.mean)
    pivot_table.columns = ['Average Sales']
    print("\nAverage sales by region:")
    print(pivot_table)

    export_to_csv(pivot_table)

    return

#Function generated by Copilot
#Function takes state, customer type, order type, and then gets the total sales for each combination
def show_sales_by_customer_and_order_type(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index=['customer_state', 'customer_type', 'order_type'], aggfunc=np.sum)
    pivot_table.columns = ['Total Sales']
    print("\nSales by customer type and order type by state:")
    print(pivot_table)

    export_to_csv(pivot_table)

    return

#Function generated by Copilot
#Function takes sales region and product then totals sales for each combination, creates pivot table of results
def show_total_sales_by_region_and_product(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index=['sales_region', 'product_category'], aggfunc=np.sum)
    pivot_table.columns = ['Total Sales']
    print("\nTotal sales quantity and price by region and product:")
    print(pivot_table)

    export_to_csv(pivot_table)

    return

#Function generated by Copilot
#Function takes each customer type and calculates total sales for each, creates pivot table of results
def show_total_sales_by_customer_type(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index='customer_type', aggfunc=np.sum)
    pivot_table.columns = ['Total Sales']
    print("\nTotal sales quantity and price by customer type:")
    print(pivot_table)

    export_to_csv(pivot_table)

    return

#Function generated by Copilot
#Function takes each product category and calculates max and min sales using numpy functions, creates pivot table of results
def show_max_min_sales_by_category(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index='product_category', aggfunc=[np.max, np.min])
    pivot_table.columns = ['Max Sales', 'Min Sales']
    print("\nMax and min sales price of sales by category:")
    print(pivot_table)

    export_to_csv(pivot_table)

    return

#Function generated by Copilot, modified because the original used Series and nunique function which I did not understand
#I converted this to an iterative approach that iterates through the dataframe and only counts unique employees in each region
#The counts are stored in a dictionary which is then passed to a new dataframe to be printed as a pivot table
def show_unique_employees_by_region(dataframe):
    region_employees = {}
    
    for _, row in dataframe.iterrows():
        region = row['sales_region']
        employee = row['employee_id']
        
        if region not in region_employees:
            region_employees[region] = []
        
        if employee not in region_employees[region]:
            region_employees[region].append(employee)

    region_counts = {}
    for region, employees in region_employees.items():
        region_counts[region] = len(employees)

    pivot_table = pd.DataFrame.from_dict(region_counts, orient='index', columns=['Unique Employees'])
    pivot_table.index.name = 'sales_region'
    print("\nNumber of unique employees by region:")
    print(pivot_table)

    export_to_csv(pivot_table)

    return

#This is a helper function created with the help of Claude to check user input to make sure that for each option in the custom pivot table process
#The user can only enter valid input otherwise they are prompted again
#My claude prompt: how would i go about checking the users input for creating the custom pivot table? because technically they could just put a number or they could have a list of numbers with valid/invalid so how would i do that
def check_user_input(user_input, valid_options, optional=False):
    if optional and not user_input.strip():
        return []  # Empty is okay for optional fields
    
    parts = [p.strip() for p in user_input.split(',') if p.strip()]  # Split, strip, remove empty parts
    if not parts and not optional:
        return None  # Required but empty
    
    selected = []
    for p in parts:
        if not p.isdigit() or p not in valid_options:
            return None  # Invalid: not a digit or not in valid options
        if p in selected:
            continue  # Skip duplicates silently (or you could error on duplicates)
        selected.append(p)
    
    return selected

def create_custom_pivot_table(dataframe):

    #Newlines added throughout for better readability
    print("Creating custom pivot table")
    print("\nAvailable rows: ")

    row_choices = ["1. employee_name", "2. sales_region", "3. product_category"]
    print("\n".join(row_choices))
    
    #Loop until valid row input
    while True:
        row_input = input("Enter the number(s) of your choice(s) for rows, separated by commas: ").strip()
        valid_rows = check_user_input(row_input, ['1', '2', '3'])
        if valid_rows is not None:
            break
        print("Invalid row selection. Please enter valid numbers (1-3) separated by commas.")
    
    print("\nAvailable columns: (optional)")

    column_choices = ["1. customer_type", "2. order_type"]

    print("\n".join(column_choices))

    #Loop until valid column input (optional)
    while True:
        column_input = input("Enter the number(s) of your choice(s) for columns, separated by commas (enter for no grouping): ").strip()
        valid_columns = check_user_input(column_input, ['1', '2'], optional=True)
        if valid_columns is not None:
            break
        print("Invalid column selection. Please enter valid numbers (1-2) separated by commas, or leave empty.")

    print("\nAvailable values: ")
    value_choices = ["1. quantity", "2. sales_price"]

    print("\n".join(value_choices))
    
    #Loop until valid value input
    while True:
        value_input = input("Enter the number(s) of your choice(s) for values, separated by commas: ").strip()
        valid_values = check_user_input(value_input, ['1', '2'])
        if valid_values is not None:
            break
        print("Invalid value selection. Please enter valid numbers (1-2) separated by commas.")

    print("\nAvailable aggregation functions: ")
    aggfunc_choices = ["1. sum", "2. mean", "3. count"]
    print("\n".join(aggfunc_choices))
    aggfunc_input = input("Enter the number(s) of your choice(s) for aggregation functions, separated by commas: ").strip()

    #I asked Claude to help me with this part because I was having trouble parsing the user input into lists that could be passed to the pivot table function
    #I didnt understand how to use the aggfunc parameter when passing multiple aggregation functions
    #Dictionaries to map user input numbers to column names and agg functions
    row_dict = {"1": "employee_name", "2": "sales_region", "3": "product_category"}
    column_dict = {"1": "customer_type", "2": "order_type"}
    value_dict = {"1": "quantity", "2": "sales_price"}
    aggfunc_dict = {"1": "sum", "2": "mean", "3": "count"}

    #Check and parse row input
    valid_rows = check_user_input(row_input, ['1', '2', '3'])
    if valid_rows is None:
        print("Invalid row selection. Please enter valid numbers (1-3) separated by commas.")
        return
    selected_rows = [row_dict[r] for r in valid_rows]

    #Check and parse column input (optional)
    valid_columns = check_user_input(column_input, ['1', '2'], optional=True)
    if valid_columns is None:
        print("Invalid column selection. Please enter valid numbers (1-2) separated by commas, or leave empty.")
        return
    selected_columns = [column_dict[c] for c in valid_columns] if valid_columns else None

    #Check and parse value input
    valid_values = check_user_input(value_input, ['1', '2'])
    if valid_values is None:
        print("Invalid value selection. Please enter valid numbers (1-2) separated by commas.")
        return
    selected_values = [value_dict[v] for v in valid_values]

    #Check and parse aggfunc input
    valid_aggfuncs = check_user_input(aggfunc_input, ['1', '2', '3'])
    if valid_aggfuncs is None:
        print("Invalid aggregation function selection. Please enter valid numbers (1-3) separated by commas.")
        return
    
    selected_aggfuncs = [aggfunc_dict[a] for a in valid_aggfuncs]

    if len(selected_aggfuncs) == 1:
        selected_aggfuncs = selected_aggfuncs[0]  # Pandas prefers string for single aggfunc
    

    #Creating the actual pivot table using the validated user input
    try:
        pivot_table = pd.pivot_table(
            dataframe,
            index=selected_rows,
            columns=selected_columns,
            values=selected_values,
            aggfunc=selected_aggfuncs
        )
        print("\nCustom Pivot Table:")
        print(pivot_table)

        export_to_csv(pivot_table)

    except Exception as e:
        print(f"Error creating pivot table: {e}")
    return


def exit_program():
    print("Exiting the program. Goodbye!")
    exit(0)

def display_menu(dataframe):
    menu_options = (
        ("Show the first n rows of the data", display_initial_rows),
        ("Show the number of employees by region", show_employees_by_region),
        ("Average sales by region with average sales by state and sale type", show_average_sales_by_region),
        ("Sales by customer type and order type by state", show_sales_by_customer_and_order_type),
        ("Total sales quantity and price by region and product", show_total_sales_by_region_and_product),
        ("Total sales quantity and price by customer type", show_total_sales_by_customer_type),
        ("Max and min sales price of sales by category", show_max_min_sales_by_category),
        ("Number of unique employees by region", show_unique_employees_by_region),
        ("Create a custom pivot table", create_custom_pivot_table),
        ("Show sales by region and product with percentage of total sales and quantity", show_sales_by_region_and_product),
        ("Exit", exit_program)
    )

    print("Available options:")
    for i, (description, _) in enumerate(menu_options, start=1):
        print(f"{i}. {description}")

    try:
        menu_len = len(menu_options)
        choice = int(input(f"Select an option (1-{menu_len}): "))
        if 1 <= choice <= menu_len-1:
            action = menu_options[choice - 1][1]
            action(dataframe)

        #This is to handle the exit option which does not require the dataframe argument and throws an error if we try to pass it in
        elif choice == menu_len:
            action = menu_options[choice - 1][1]
            action()

        else:
            print("Invalid choice. Please select a valid option.")
    
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the menu options.")

def main():
    while True:
        print("\n____Sales Data Dashboard____")
        display_menu(sales_data)


filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"
sales_data = load_csv(filename)

# Check if this is the main module being run
if __name__ == "__main__":
    main()