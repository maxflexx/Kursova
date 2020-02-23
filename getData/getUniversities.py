import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://studyinukraine.gov.ua/en/study-in-ukraine/universities'

response = requests.get(url)
soup = BeautifulSoup(response.text)
names = soup.findAll('h3')
print(names)
univ = []
for name in names:
	if len(name.contents) > 0:
		try:
			univ.append(name.contents[0].contents[0])
		except:
			univ.append(name.contents[0])

with open("universities.txt", "w") as f:
	f.write("\n".join(univ))