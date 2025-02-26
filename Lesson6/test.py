# import requests
# from bs4 import BeautifulSoup
#
# URL = "https://habr.com/ru/news"
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
# }
#
# def get_news():
#     response = requests.get(URL, headers=HEADERS)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "lxml")
#         articles = soup.find_all("a", class_="tm-title__link")
#
#         news_list = []
#         for article in articles[:10]:
#             title = article.text.strip()
#             link = "https://habr.com" + article["href"]
#             news_list.append(f"{title}\n{link}")
#         return "\n\n".join(news_list)
#     else:
#         return "Ошибка при получении данных"
#
# print(get_news())