from bs4 import BeautifulSoup
import requests


resp = requests.get("https://ru.wikipedia.org")
html = resp.text

soup = BeautifulSoup(html, 'lxml')
tags = soup("a", "extiw")
links = [tag["href"] for tag in tags]

print(links)