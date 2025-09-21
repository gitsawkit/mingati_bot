import os
import pytest
from mistralai import Mistral
import discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_SECRET_CLIENT")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Tests Mistral API
def test_mistral_connection():
    """Test de connexion à l'API Mistral"""
    try:
        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": "Test ping"}]
        )
        assert response and hasattr(response, "choices")
        assert len(response.choices) > 0
    except Exception as e:
        pytest.fail(f"❌ Échec de connexion à Mistral : {e}")

# Tests Discord API
@pytest.mark.asyncio
async def test_discord_connection():
    """Test de connexion à l'API Discord"""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        await bot.close()

    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        pytest.fail(f"❌ Échec de connexion à Discord : {e}")