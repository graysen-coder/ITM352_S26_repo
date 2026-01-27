#Name: Graysen Oumi
#Date: Jan 22, 2026

def convertToCelsius(temperature):
    """
    Convert a temperature from Fahrenheit to Celsius.
    Formula: C = (F - 32) * 5/9
    """
    celsius_value = (temperature - 32) * 5 / 9
    celsius_value_rounded = round(celsius_value, 2)
    return celsius_value_rounded

"""
# Main program
fahrenheit_input = input("Please enter a temperature in Fahrenheit: ")
fahrenheit_float = float(fahrenheit_input)
result = convertToCelsius(fahrenheit_float)

print("You entered:", fahrenheit_input)
print(f"The temperature in Celsius is: {result}")

"""
userTemp = input("Please enter a temperature in Fahrenheit: ")
userTemp_float = float(userTemp)
result = convertToCelsius(userTemp_float)
print(result)