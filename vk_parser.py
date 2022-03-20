import requests
from bs4 import BeautifulSoup
import json


def get_first_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    url = "https://www.ixbt.com/news/"
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    post = soup.find_all("li", class_="item")
    news_dict = {}
    for el in post:
        post_text = el.find("strong").text
        link = el.find("a", href=True).get('href')
        post_time = el.find("span", class_="time_iteration_icon_light").text
        if len(str(post_time)) > 5:
            post_time = post_time[-5:]
        # print(post_time, post_text, "https://ixbt.com"+link, sep="\n")
        news_dict[post_time] = {
            "post_time": post_time,
            "text": post_text,
            "link": link,
        }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    url = "https://www.ixbt.com/news/"
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    post = soup.find_all("li", class_="item")
    fresh_news = {}
    for el in post:
        post_time = el.find("span", class_="time_iteration_icon_light").text
        if len(str(post_time)) > 5:
            post_time = post_time[-5:]
        if post_time in news_dict:
            continue
        else:
            post_text = el.find("strong").text
            link = el.find("a", href=True).get('href')
            post_time = el.find("span", class_="time_iteration_icon_light").text
            if len(str(post_time)) > 5:
                post_time = post_time[-5:]
            news_dict[post_time] = {
                "post_time": post_time,
                "text": post_text,
                "link": link
            }
            fresh_news[post_time] = {
                "post_time": post_time,
                "text": post_text,
                "link": link
            }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    return fresh_news



def main():
    print(check_news_update())


if __name__ == '__main__':
    main()








