import requests
from bs4 import BeautifulSoup

# 1. Fetch the page
url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
headers = {"User-Agent": "Mozilla/5.0"}  # Some sites block requests without a user-agent
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raises an error if the request failed

# 2. Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# 3. Find the rate table — inspect the page to confirm the tag/class
table = soup.find("table")  # or soup.find("table", class_="some-class") if needed

# 4. Extract and print each row
if table:
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all(["td", "th"])  # grab both header and data cells
        values = [col.get_text(strip=True) for col in cols]
        if values:
            print(" | ".join(values))
else:
    print("No table found — the structure may require inspection.")