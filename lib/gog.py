import logging
import requests
from bs4 import BeautifulSoup


def get_free_games():
    url = "https://www.gog.com/fr/games?priceRange=0,0&discounted=true"
    headers = {"User-agent": "Mozilla/5.0"}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    logging.info("🔎 Recherche de jeux gratuit sur GoG...")
    for result in soup.find_all("a", class_="product-tile product-tile--grid"):
        title_tag = result.find("div", class_="product-tile__title ng-star-inserted")
        if title_tag:
            game = {
                "platform": "GoG",
                "icon": "<:gog:1447059257211224155>",
                "title": title_tag["title"],
                "link": result["href"],
                "expired_date": None
            }
            games.append(game)
            logging.debug(f"➕ Ajouté : {game['title']} ({game['link']})")

    logging.info(f"👮 Recherche terminé, {len(games)} jeux trouvés.")
    return games