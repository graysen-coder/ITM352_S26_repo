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

#turn this into a function that takes a list of purchases and a budget as parameters and returns the total spent and whether it is over budget or not.

def check_budget(purchases, budget):
    total_spent = 0

    for purchase in purchases:

        total_spent += purchase

    is_over_budget = total_spent > budget

    return total_spent, is_over_budget

# Write 5 test cases for the check_budget function using the assert statement to verify the expected output.
# The tests cases should cover total spent being under budget, exactly at budget, over budget, getting an empty purchases list, and negative purchase amounts

# Test case 1: Total spent is under budget
purchases1 = [2.99, 5.49, 1.50]
budget1 = 10
total1, over_budget1 = check_budget(purchases1, budget1)
assert total1 == 9.98, f"Expected total spent to be 9.98, got {total1}"
assert over_budget1 == False, f"Expected over budget to be False, got {over_budget1}"

# Test case 2: Total spent is exactly at budget
purchases2 = [2.99, 5.49, 1.52]
budget2 = 10
total2, over_budget2 = check_budget(purchases2, budget2)
assert total2 == 10.00, f"Expected total spent to be 10.00, got {total2}"
assert over_budget2 == False, f"Expected over budget to be False, got {over_budget2}"

# Test case 3: Total spent is over budget
purchases3 = [2.99, 5.49, 1.50, 3.25]
budget3 = 10
total3, over_budget3 = check_budget(purchases3, budget3)
assert total3 == 13.23, f"Expected total spent to be 13.23, got {total3}"
assert over_budget3 == True, f"Expected over budget to be True, got {over_budget3}"

# Test case 4: Empty purchases list
purchases4 = []
budget4 = 10
total4, over_budget4 = check_budget(purchases4, budget4)
assert total4 == 0, f"Expected total spent to be 0, got {total4}"
assert over_budget4 == False, f"Expected over budget to be False, got {over_budget4}"

# Test case 5: All purchases are negative amounts
purchases5 = [-2.99, -5.49, -1.50]
budget5 = 10
total5, over_budget5 = check_budget(purchases5, budget5)
assert total5 == -9.98, f"Expected total spent to be -9.98, got {total5}"
assert over_budget5 == False, f"Expected over budget to be False, got {over_budget5}"
print("All test cases passed!")

