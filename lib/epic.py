import epicstore_api


api = epicstore_api.EpicGamesStoreAPI()


def get_free_games():
    games = []
    print("🔎 Recherche de jeux gratuits sur Epic Games...")

    free_games = api.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]

    for game in free_games:
        title = game["title"]
        product_slug = game.get("productSlug")
        link = f"https://store.epicgames.com/fr/p/{product_slug}"
        expired_date = game['expiryDate']

        if product_slug is not None and expired_date is not None :
            game_data = {
                "platform": "Epic Games",
                "title": title,
                "link": link,
                "expired_date": expired_date
            }
            games.append(game_data)

    print(f"👮‍♂️ Recherche terminée, {len(games)} jeux trouvés.")
    return games