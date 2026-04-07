#Parse the ITM Deparment website to find the people 
import urllib.request
from bs4 import BeautifulSoup

itm_url = "https://shidler.hawaii.edu/itm/people"

itm_html = urllib.request.urlopen(itm_url)

html_to_parse = BeautifulSoup(itm_html, 'html.parser')

#print(html_to_parse.find_all("h2", class_="title"))

list_of_faculty = html_to_parse

itm_faculty = []
for person in list_of_faculty:
    itm_faculty.append
    print(person.text.strip())

unique_faculty = set(itm_faculty)
print(f"Unique faculty members: {len(unique_faculty)}")