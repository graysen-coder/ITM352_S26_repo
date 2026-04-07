# Grab 1 month interest rate data from the treasury website
import ssl
import pandas as pd
import urllib.request
import lxml

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"
ssl_create_default_https_context = ssl._create_unverified_context

print("Opening URL: ", url)
web_page = urllib.request.urlopen(url)
data_frame = pd.read_html(web_page)

print(data_frame[0])

#Extract the 1 month interest rate data
one_month_rate = data_frame[0].loc[0, "1 Mo"]
print(f"1 month interest rate on 2026-03-01: {one_month_rate}")

