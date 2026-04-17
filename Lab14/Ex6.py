#Create a scatter plot of fares by trip miles based on “Trips from area 8.json”.
#Save the plot to a file called FaresXmiles.png
#Filter out trips of 0 miles.
#Filter out trips less than 2 miles.
#What anomalies do you notice in the data?

import json
import matplotlib.pyplot as plt

with open("Trips from area 8.json") as f:
    data = json.load(f)

fares = []
trip_miles = []

for trip in data:
    if "fare" in trip and "trip_miles" in trip:
        fare = float(trip["fare"])
        miles = float(trip["trip_miles"])
        if miles >= 2:  # Filter out trips of 0 miles and less than 2 miles
            fares.append(fare)
            trip_miles.append(miles)

plt.scatter(fares, trip_miles)
plt.xlabel("Fare")
plt.ylabel("Trip Miles")
plt.title("Scatter Plot of Fares and Trip Miles")
plt.savefig("FaresXmiles.png")
plt.show()

# Anomalies: even after removing trips under 2 miles, some rides still have high fares for short distances, indicating an irregular fare-per-mile ratio or extra charges.
