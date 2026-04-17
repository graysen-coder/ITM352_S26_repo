#Create a scatter plot of fares by trip miles based on “Trips from area 8.json”.
#Put the fare on the X axis and the trip miles on the Y axis.  Use plt.scatter().
#Now create the same scatter plot using plt.plot with linestyle= "none" and marker="."
#Now make the plot fancier, with a “v” marker, cyan color, and 0.2 transparency.
#What conclusions can you draw about this data?

import json
import matplotlib.pyplot as plt

with open("Trips from area 8.json") as f:
    data = json.load(f)
fares = []
trip_miles = []

for trip in data:
    if "fare" in trip and "trip_miles" in trip:
        fares.append(float(trip["fare"]))
        trip_miles.append(float(trip["trip_miles"]))

# 1) scatter plot using plt.scatter()
plt.figure()
plt.scatter(fares, trip_miles)
plt.xlabel("Fare")
plt.ylabel("Trip Miles")
plt.title("Scatter Plot of Fares and Trip Miles")
plt.show()

# 2) same scatter plot using plt.plot()
plt.figure()
plt.plot(fares, trip_miles, linestyle="none", marker=".")
plt.xlabel("Fare")
plt.ylabel("Trip Miles")
plt.title("Scatter Plot of Fares and Trip Miles (plt.plot)")
plt.show()

# 3) fancier version with a cyan 'v' marker and transparency
plt.figure()
plt.plot(fares, trip_miles, linestyle="none", marker="v", color="cyan", alpha=0.2)
plt.xlabel("Fare")
plt.ylabel("Trip Miles")
plt.title("Fancy Scatter Plot of Fares and Trip Miles")
plt.show()
