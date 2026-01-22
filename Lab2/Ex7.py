#Ask the user to enter a temperature in fahrenheit
#Convert the temperature to celsius using the formula C = (F - 32) * 5/9
#Name: Graysen Oumi
#Date: Jan 22, 2026

fahrenheit_input = input("Please enter a temperature in Fahrenheit: ")
fahrenheit_float = float(fahrenheit_input)
celsius_value = (fahrenheit_float - 32) * 5 / 9
celsius_value_rounded = round(celsius_value, 2)

print("You entered:", fahrenheit_input)
print(f"The temperature in Celsius is: {celsius_value_rounded}")

