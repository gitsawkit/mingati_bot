import discord
from discord.ext import commands
import os


TOKEN = os.getenv("DISCORD_SECRET_CLIENT")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Le bot est prêt ! Connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message de {message.author}: {message.content}")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Salut !")

if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR : DISCORD_SECRET_CLIENT - Le token du bot Discord est manquant.")