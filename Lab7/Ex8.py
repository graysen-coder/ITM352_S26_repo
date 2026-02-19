recent_purchase = [2.99, 5.49, 1.50, 3.25]
budget = 10
total_spent = 0

total_spent = 0

for purchase in recent_purchase:
    total_spent += purchase
    if total_spent > budget:
        print("This purchase is over budget!", purchase)

    else:
        print("This purchase is within budget.", purchase)
