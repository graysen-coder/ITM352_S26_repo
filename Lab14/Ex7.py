#Create a 3D plot of fares, trip miles and dropoff area based on “Trips from area 8.json”. To do this you will need to add this line to your code: 
from mpl_toolkits.mplot3d import Axes3D

#Put the fare on the X axis, trip miles on the Y axis and dropoff area on the Z axis.
#Use plt.scatter() to create the plot.  Use a different color for each dropoff area.
import json
import matplotlib.pyplot as plt
with open("Trips from area 8.json") as f:
    data = json.load(f)
fares = []
trip_miles = []
dropoff_areas = []

for trip in data:
    if "fare" in trip and "trip_miles" in trip and "dropoff_community_area" in trip:
        fares.append(float(trip["fare"]))
        trip_miles.append(float(trip["trip_miles"]))
        dropoff_areas.append(int(trip["dropoff_community_area"]))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(fares, trip_miles, dropoff_areas, c=dropoff_areas, cmap='viridis')
ax.set_xlabel("Fare")
ax.set_ylabel("Trip Miles")
ax.set_zlabel("Dropoff Area")
ax.set_title("3D Scatter Plot of Fares, Trip Miles and Dropoff Area")
legend1 = ax.legend(*scatter.legend_elements(), title="Dropoff Areas")
ax.add_artist(legend1)
plt.show()
