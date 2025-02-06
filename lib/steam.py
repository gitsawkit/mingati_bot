import requests
from bs4 import BeautifulSoup


def get_free_games():
    url = "https://store.steampowered.com/search/?maxprice=free&specials=1&ndl=1"
    headers = {"User-agent": "Mozilla/5.0"}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    print("🔎 Recherche de jeux gratuit sur Steam...")
    for result in soup.find_all("a", class_="search_result_row"):
        title_tag = result.find("span", class_="title")
        image_tag = result.find("img")
        if title_tag and image_tag:
            game = {
                "platform": "Steam",
                "title": title_tag.text,
                "link": result["href"],
                "image": image_tag["src"],
                "expired_date": None
            }
            games.append(game)

    print(f"✅ Recherche terminé. {len(games)} jeux trouvés :\n {games}")
    return games