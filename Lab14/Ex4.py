#Create a scatter plot of fares and tips from the file “Trips_Fri07072017T4 trip_miles gt1.json”.
#Put the fare on the X axis and tips on the Y axis.
#What conclusions can you draw about the data from this scatter plot?
import json
import matplotlib.pyplot as plt

with open("Trips_Fri07072017T4 trip_miles gt1.json") as f:
    data = json.load(f)

fares = []
tips = []

for trip in data:
    if "fare" in trip and "tips" in trip:
        fares.append(float(trip["fare"]))
        tips.append(float(trip["tips"]))

plt.scatter(fares, tips)
plt.xlabel("Fare")
plt.ylabel("Tips")
plt.title("Scatter Plot of Fares and Tips")
plt.show()
