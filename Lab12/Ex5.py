#Get a JSON file from the City of Chicago's Data portal and analysis driver types

import pandas as pd
import requests

#Create a REST query to get the JSON data for driver types

search_results = requests.get("https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type")

results_json = search_results.json()
print("Driver types and their counts:")
print(results_json)

#Convert the JSON data to a DataFrame
df = pd.DataFrame(results_json)
df.columns = ["driver_type", "count"]
df = df.set_index("driver_type")

print("\nVarious types and their counts (Dataframe)")
print(df)