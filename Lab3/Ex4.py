#Handy library of math functions
#Name: Graysen Oumi
#Date: Jan 27, 2026

def midpoint(num1,num2):
    """Calculate the midpoint between two numbers."""
    mid = (num1 + num2) / 2
    return mid

def sqrt(number):
    """Calculate the square root of a number."""
    if number < 0:
        return None
    return number ** 0.5

def exponent(base, power, precision):
    """Calculate the exponentiation of a base raised to a power."""
    result = base ** power
    rounded_result = round(result, precision)
    return rounded_result
