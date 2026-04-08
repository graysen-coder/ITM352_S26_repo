#Get public license data from the City of Chicago's Data portal

import pandas as pd
from sodapy import Socrata

#Create a Socrata client to access the City of Chicago's Data portal
client = Socrata("data.cityofchicago.org", None)

#Specify the JSON file for licenses data
json_file = "rr23-ymwb"

results = client.get(json_file, limit=500)

df = pd.DataFrame.from_records(results)

print(df.head())

vehicles_and_fuel_sources = df[["public_vehicle_number", "vehicle_fuel_source"]]
print("Public Vehicle Number and Fuel Source:")
print(vehicles_and_fuel_sources)

vehicles_by_fuel_source = vehicles_and_fuel_sources.groupby("vehicle_fuel_source").count()
print(vehicles_by_fuel_source)