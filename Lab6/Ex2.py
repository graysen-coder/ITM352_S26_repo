#Write Python code that creates a list with a variety of different values. 
# Include control logic (if, elif, else) that will print different messages whether the list 
# contains fewer than 5 elements, between 5 and 10 (inclusive), and more than 10 elements. 
# Test your code on lists with several different lengths.


#Generate a list of lists with different lengths to test the control logic
test_list = [[1, 2], [3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16], [17, 18, 19, 20, 21, 22, 23, 24, 25]]

def check_list_length(lst):
    # Check for fewer than 5 elements
    if len(lst) < 5:
        print("The list contains fewer than 5 elements.")
    
    # Check for between 5 and 10 elements (inclusive)
    elif 5 <= len(lst) <= 10:
        print("The list contains between 5 and 10 elements.")
    
    # Check for more than 10 elements
    else:
        print("The list contains more than 10 elements.")

# Loop through test_list and use the function on every list within test_list
for sublist in test_list:
    check_list_length(sublist)
