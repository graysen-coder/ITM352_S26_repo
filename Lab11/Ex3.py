#Read in a csv file and create a dataframe
# Pivot the dataframe, aggregating sales by region with columns defined by order_type and totals

import pandas as pd
import numpy as np

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd.set_option('display.max_columns', None)  # Show all columns in the output
pd.set_option('display.float_format', lambda x: f'{x:.2f}')  # Format floats to 2 decimal places

df = pd.read_csv(filename)
df["order_date"] = pd.to_datetime(df["order_date"], format="%d-%m-%Y", errors='coerce')

df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce')
df["unit_price"] = pd.to_numeric(df["unit_price"], errors='coerce')
df["sales"] = df["quantity"] * df["unit_price"]

pivot_table = pd.pivot_table(df,
                             index="sales_region",
                             values="sales",
                             columns=["order_type", state_col],
                             aggfunc=[np.sum, np.mean],
                             margins=True,
                             margins_name="Total Sales")

print(pivot_table)