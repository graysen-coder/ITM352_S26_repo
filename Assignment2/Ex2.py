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

print(sales_data.head(10))