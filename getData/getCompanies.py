import requests
import urllib.request
from bs4 import BeautifulSoup

companies_html = ""
companies = []
with open("company.txt", "r") as f:
	companies_html = f.read()



soup = BeautifulSoup(companies_html)
mydivs = soup.findAll("a", {"class": "cn-a"})
for d in mydivs:
	try:
		companies.append(d.contents[0])
	except:
		print("fail")

with open("companies.txt", "w") as f:
	f.write("\n".join(companies))
