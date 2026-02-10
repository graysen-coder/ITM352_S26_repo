trip_duration = [1.1, 0.8, 2.5, 2.6]
trip_fare = (6.25, 5.25, 10.50, 8.05)

# Normalize fares to numbers (handles strings or numeric types)
normalized_fares = [float(f) for f in trip_fare]

# Build a list of dictionaries from the two sequences
trips_list = [{"duration": d, "fare": f} for d, f in zip(trip_duration, normalized_fares)]

# Print duration and cost of the 3rd trip (index 2)
third_trip = trips_list[2]
print(f"Duration: {third_trip['duration']} miles")
print(f"Fare: ${third_trip['fare']:.2f}")
