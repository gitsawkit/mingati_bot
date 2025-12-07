import epicstore_api
import logging
from datetime import datetime, timedelta


api = epicstore_api.EpicGamesStoreAPI()
current_time = (datetime.utcnow() + timedelta(hours=1)).isoformat() + 'Z'

def get_free_games():
    games = []
    logging.info("🔎 Recherche de jeux gratuits sur Epic Games...")

    free_games = api.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]

    for game in free_games:
        title = game["title"]
        logging.debug(f"\n🎮 Analyse de {title}")

        promotions = game.get('promotions')
        if not promotions:
            logging.debug(f"Pas de promotions pour {title}")
            continue

        promotional_offers = promotions.get('promotionalOffers', [])
        if not promotional_offers:
            logging.debug(f"Pas d'offres promotionnelles pour {title}")
            continue

        price = game.get('price', {}).get('totalPrice', {})
        discount_price = price.get('discountPrice', 0)
        logging.debug(f"Prix avec réduction : {discount_price}")

        for offer in promotional_offers:
            for promo in offer.get('promotionalOffers', []):
                start_date = datetime.fromisoformat(promo.get('startDate').replace('Z', ''))
                start_date = (start_date + timedelta(hours=1)).isoformat() + 'Z'
                end_date = datetime.fromisoformat(promo.get('endDate').replace('Z', ''))
                end_date = (end_date + timedelta(hours=1)).isoformat() + 'Z'

                logging.debug(f"Promotion trouvée:")
                logging.debug(f"  - Dates: {start_date} -> {end_date}")

                if discount_price == 0:
                    if start_date <= current_time <= end_date:
                        logging.debug(f"✅ {title} est actuellement gratuit!")

                        mappings = game.get("catalogNs", {}).get("mappings", [])
                        if mappings and mappings[0].get("pageSlug"):
                            page_slug = mappings[0]["pageSlug"]
                            link = f"https://store.epicgames.com/fr/p/{page_slug}"

                            game_data = {
                                "platform": "Epic Games",
                                "icon": "<:epic_games:1447060063553585152>",
                                "title": title,
                                "link": link,
                                "expired_date": end_date
                            }
                            games.append(game_data)
                            logging.debug(f"➕ Ajouté : {title} ({link})")

    logging.info(f"👮 Recherche terminée, {len(games)} jeux trouvés.")
    return games