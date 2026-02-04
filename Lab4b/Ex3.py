#Parse trought the portions of an email address

email = input("Enter your email address: ")

parts = email.split("@")
username = parts[0]
domain = parts[1]

print("Username:", username)
print("Domain:", domain)

#Method 2: using index() and slicing
at_symbol_index = email.index("@")
username_email = email[:at_symbol_index]
domain_email = email[at_symbol_index + 1:]

print("Username (manual):", username_email)
print("Domain (manual):", domain_email)