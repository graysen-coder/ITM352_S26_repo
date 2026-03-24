#Read a json file of taxi trip data and create a dataframe
#Calculate the median fare

import json
import pandas as pd

taxi_df = pd.read_json("Taxi_Trips.json")
print(taxi_df.describe())

print(taxi_df.head())
median_fare = taxi_df["fare"].median()
print("Median fare:", f"{median_fare:.2f}")