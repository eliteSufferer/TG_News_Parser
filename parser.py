import requests
from bs4 import BeautifulSoup


url = "https://www.securitylab.ru/news/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
title = soup.find("h2", class_="article-card-title").text.strip()
print(title)

'''
url = "https://habr.com/ru/search/?q=python&target_type=posts&order=relevance"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
post = soup.find("article", class_="tm-articles-list__item", id.txt=True)
title = post.find("h2", class_="tm-article-snippet__title tm-article-snippet__title_h2").text.strip()
print(title)
'''
