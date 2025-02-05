import discord, os, random
from discord.ext import commands


DISCORD_TOKEN = os.getenv("DISCORD_SECRET_CLIENT")

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

    if bot.user.mentioned_in(message):
        print(f"{message.author} me parle !")

    print(f"Message de {message.author}: {message.content}")

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    welcome_channel: discord.TextChannel = bot.get_channel("933379075995758603")

    messages = [
        f"Bienvenue {member.display_name} ! 😬",
        f"Est-ce un oiseau ? Un avion ?! Mais non, c'est {member.display_name} !",
        f"Saint pétard ti, vla {member.display_name} ! On est foutus...",
        f"Si on m'avait dit que je verrai {member.display_name} un jour... 😏",
        f"{member.display_name} vient d'entrer dans l'arène ! Espérons qu'il survive 🤞",
        f"Oh non... Pas encore un {member.display_name}... On en avait pas déjà un en stock ? 😆",
        f"La légende disait vrai... {member.display_name} existe vraiment 👀",
        f"{member.display_name} a été invoqué avec succès !",
        f"On pensait être tranquilles... et voilà que {member.display_name} arrive 😬",
    ]

    await welcome_channel.send(random.choice(messages))


if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("ERROR : DISCORD_SECRET_CLIENT - Le token du bot Discord est manquant.")