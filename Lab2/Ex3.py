#Ask the user to enter a floating point number, square the
#number print out the original number and the squared result
#Name: Graysen Oumi
#Date: Jan 22, 2026

#Asking the user to enter a floating point number
input_value = input("Please enter a floating point number: ")

#Conversion of the data type and squaring the number
float_value = float(input_value)
squared_result = float_value ** 2

#Round the number to 2 decimal places
squared_result = round(squared_result, 2)

print("You entered:", input_value)
print(f"The squared value is: {squared_result}")