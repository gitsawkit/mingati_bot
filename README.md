# Mingati Bot

Un bot Discord intelligent utilisant l'API Mistral pour des interactions conversationnelles avancées.

## 🚀 Démarrage rapide

### Prérequis

- Docker et Docker Compose
- Clés API Discord et Mistral

### Configuration

1. **Clonez le repository**
   ```bash
   git clone https://github.com/gitsawkit/mingati_bot.git
   cd mingati_bot
   ```

2. **Configurez les variables d'environnement**
   
   Introduire les clés API dans un fichier `.env`, comme ceci :
   ```
   DISCORD_SECRET_CLIENT=XXXX
   MISTRAL_API_KEY=XXXX
   ```

### 🛠️ Développement

Pour lancer le bot en mode développement :

```bash
docker compose up -d --build mingati_bot_dev
```

### 🚀 Production

Pour déployer le bot en production :

```bash
docker compose up -d --build mingati_bot_prod
```

## 📝 Commandes utiles

- **Voir les logs** : `docker compose logs -f mingati_bot_prod` (ou `mingati_bot_dev`)
- **Arrêter le bot** : `docker compose down`
- **Redémarrer** : `docker compose restart mingati_bot_prod`

## 🔧 Technologies utilisées

- **Discord.py** - Framework pour les bots Discord
- **Mistral AI** - Modèle de langage pour les réponses intelligentes
- **Docker** - Containerisation pour un déploiement facile

## 📋 Notes

- Assurez-vous que votre bot Discord a les permissions nécessaires sur votre serveur
- Les clés API doivent être gardées secrètes et ne jamais être commitées dans le repository

---

*Développé avec ❤️ par [SAWKIT](https://github.com/gitsawkit)*
