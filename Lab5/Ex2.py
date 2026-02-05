trip_duration = [1.1, 0.8, 2.5, 2.6]
trip_fare = (6.25, 5.25, 10.50, 8.05)

taxitrips = {
    "miles": trip_duration,
    "fares": trip_fare
}

print(taxitrips)

print(f"The third trip was {taxitrips['miles'][2]} miles long")
print(f"The fare for the third trips was ${taxitrips['fares'][2]:.2f}")

