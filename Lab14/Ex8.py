#Create a heatmap from pickup_community_area and dropoff_community_area based on “taxi trips Fri 7_7_2017.csv”
import json
import matplotlib.pyplot as plt
import seaborn as sns
with open("Trips from area 8.json") as f:
    data = json.load(f)
pickup_areas = []
dropoff_areas = []
for trip in data:
    if "pickup_community_area" in trip and "dropoff_community_area" in trip:
        pickup_areas.append(int(trip["pickup_community_area"]))
        dropoff_areas.append(int(trip["dropoff_community_area"]))
heatmap_data = {}
for pickup, dropoff in zip(pickup_areas, dropoff_areas):
    if pickup not in heatmap_data:
        heatmap_data[pickup] = {}
    if dropoff not in heatmap_data[pickup]:
        heatmap_data[pickup][dropoff] = 0
    heatmap_data[pickup][dropoff] += 1
heatmap_matrix = []
pickup_labels = sorted(heatmap_data.keys())
dropoff_labels = sorted({dropoff for pickup in heatmap_data.values() for dropoff in pickup.keys()})
for pickup in pickup_labels:
    row = []
    for dropoff in dropoff_labels:
        row.append(heatmap_data.get(pickup, {}).get(dropoff, 0))
    heatmap_matrix.append(row)
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_matrix, xticklabels=dropoff_labels, yticklabels=pickup_labels, cmap="YlGnBu")
plt.xlabel("Dropoff Community Area")
plt.ylabel("Pickup Community Area")
plt.title("Heatmap of Pickup and Dropoff Community Areas")
plt.show()
