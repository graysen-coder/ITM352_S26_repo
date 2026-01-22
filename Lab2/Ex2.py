#Ask the user to enter their bith year. Calculate their age in the current year (2026)
#and print it out
#Name: Graysen Oumi
#Date: Jan 20, 2026

birth_year = input("Please enter your birth year: ")
birth_year_int = int(birth_year)
current_year = 2026
and_age = current_year - birth_year_int
print("You entered: ", birth_year_int)
print(f"You are {and_age} years old.")