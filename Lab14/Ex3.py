#Create a second histogram from the trip miles data found in the file “Trips from area 8.json”.
#Use payment method as the X axis and (sum of) tips as the Y axis.  
#Drop rows with NA values.
#Assign appropriate labels and a title to the plot
import json
import matplotlib.pyplot as plt

with open("Trips from area 8.json") as f:
    data = json.load(f)

payment_methods = {}
for trip in data:
    if "payment_type" in trip and "tips" in trip:
        payment_method = trip["payment_type"]
        tip_amount = float(trip["tips"])
        payment_methods[payment_method] = payment_methods.get(payment_method, 0) + tip_amount

plt.bar(payment_methods.keys(), payment_methods.values())
plt.xlabel("Payment Method")
plt.ylabel("Total Tips")
plt.title("Total Tips by Payment Method")
plt.xticks(rotation=45)
plt.show()