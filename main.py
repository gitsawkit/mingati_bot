import discord
from discord.ext import commands
import os


TOKEN = os.getenv("DISCORD_SECRET_CLIENT")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Le bot est prêt ! Connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(f"<@{bot.user.id}>"):
        print(f"{message.author} me parle !")

    print(f"Message de {message.author}: {message.content}")

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    welcome_channel: discord.TextChannel = bot.get_channel("933379075995758603")
    await welcome_channel.send(f"Bienvenue {member.display_name} !")

if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR : DISCORD_SECRET_CLIENT - Le token du bot Discord est manquant.")