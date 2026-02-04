url = input("Enter a URL: ")

cleaned_url = url.replace("https://", "")

print("Cleaned URL:", cleaned_url)

parts = cleaned_url.split("/")

domain = parts[2]
print("Domain:", domain)

TLD = domain.split(".")[-1]

# might get a trailing / character, if so need to remove it
#TLD_clean = TLD.strip("/")

TLD_clean = TLD.replace("/", "")
print("Top-Level Domain (TLD):", TLD_clean)