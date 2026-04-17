#Create a histogram from the trip miles data found in the file “Trips from area 8.json”.    
#Use trip miles as the X axis and frequency as the Y axis.
import json
import matplotlib.pyplot as plt

with open("Trips from area 8.json") as f:
    data = json.load(f)

trip_miles = [trip["trip_miles"] for trip in data]

plt.hist(trip_miles, bins=20)
plt.xlabel("Trip Miles")
plt.ylabel("Frequency")
plt.title("Distribution of Trip Miles")
plt.show()


