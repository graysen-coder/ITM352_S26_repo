prices = (100, 10, 50, 25, 75)

total = 0

for price in prices:
    item_count = 3
    if item_count > 2:
        discounted_price = price * 0.8  # Apply a 20% discount

    else:
        discounted_price = price
    total += discounted_price

rounded_total = round(total, 2)  # Round to 2 decimal places

print(f"Total price: ${rounded_total:.2f}")
