#Name: Graysen Oumi
#Date: Jan 29, 2026
#1. Use the input() function learned in Chapter 2 to input three strings 
# (a first name, a middle initial, and a last name). 
# Concatenate these strings together with a space between each, 
# storing the result in a new variable. Print out the concatenated string.


firstName = "Graysen"
middleName = "Kazushige"
lastName = "Oumi"

'''a. Do this using the “+” concatenation operator. Explain how Python 
knows this is different than adding two numbers together.
'''

plus_full_string = firstName + " " + middleName + " " + lastName
print(plus_full_string)

#b. Do this using an f-string 
fstring_full_string = f"{firstName} {middleName} {lastName}"
print(fstring_full_string)

#c. Do this using the % Operator
percent_full_string = "%s %s %s" % (firstName, middleName, lastName)
print(percent_full_string)

#d. Do this using the format() method for a string
format_full_string = "{} {} {}".format(firstName, middleName, lastName)
print(format_full_string)

#e. Do this using a join() method of a list
list_full_string = " ".join([firstName, middleName, lastName])
print(list_full_string)

#f. Do this using the format() method for a string but unpacking the list as the argument
unpack_full_string = "{} {} {}".format(*[firstName, middleName, lastName])
print(unpack_full_string)