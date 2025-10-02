# Mingati Bot

Un bot Discord intelligent utilisant l'API Google Gemini pour des interactions conversationnelles avancées.

## 🚀 Démarrage rapide

### Prérequis

- Docker et Docker Compose
- Clés API Discord et Google Gemini

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
   GEMINI_API_KEY=XXXX
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
- **Google Gemini** - Modèle de langage pour les réponses intelligentes
- **Docker** - Containerisation pour un déploiement facile

## 🧪 Tests

### Tests manuels

Pour tester l'interaction avec l'API Gemini manuellement :

```bash
python debug/ai.py
```

Cela lancera une session interactive où vous pourrez discuter avec le bot. Pour quitter, tapez "bye", "au revoir", "quitter" ou "exit".

### Tests automatisés

Pour exécuter les tests automatisés :

```bash
pytest debug/ai.py -v
```

Les tests vérifient :
- La connexion à l'API Gemini
- Les interactions de base du bot
- Le formatage des réponses

## 📋 Notes

- Assurez-vous que votre bot Discord a les permissions nécessaires sur votre serveur
- Les clés API doivent être gardées secrètes et ne jamais être commitées dans le repository
- Pour les tests, assurez-vous que la variable d'environnement `GEMINI_API_KEY` est configurée

---

*Développé avec ❤️ par [SAWKIT](https://github.com/gitsawkit)*
