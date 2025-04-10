import discord, json, os, random
from datetime import datetime
from discord.ext import commands, tasks
from lib import steam, gog, epic


DISCORD_TOKEN = os.getenv("DISCORD_SECRET_CLIENT")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

SENT_GAMES_FILE = os.path.join("data", ".sent_games.json")
MAX_GAMES_STORE = 30


@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

    if not check_free_games.is_running():
        check_free_games.start()


@bot.event
async def on_message(message):
    print(f"💬 Message de {message.author}:\n{message.content}\n------")

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        message.content = message.content.replace(f"<@{bot.user.id}>", "")
        message.content = message.content.strip()

        if message.content.startswith("dis à") or message.content.startswith("dis"):
            if message.content.startswith("dis à"):
                message.content = message.content.replace("dis à", "")
            else:
                message.content = message.content.replace("dis", "")

            message.content = message.content.strip()

            await message.delete()
            await message.channel.send(message.content)

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    welcome_channel: discord.TextChannel = bot.get_channel(1049796965334011945)

    messages = [
        f"Bienvenue @{member.display_name} ! 😬",
        f"Est-ce un oiseau ? Un avion ?! Mais non, c'est @{member.display_name} !",
        f"Saint pétard ti, vla @{member.display_name} ! On est foutus...",
        f"Si on m'avait dit que je verrai @{member.display_name} un jour... 😏",
        f"@{member.display_name} vient d'entrer dans l'arène ! Espérons qu'il survive 🤞",
        f"Oh non... Pas encore un @{member.display_name}... On en avait pas déjà un en stock ? 😆",
        f"La légende disait vrai... @{member.display_name} existe vraiment 👀",
        f"@{member.display_name} a été invoqué avec succès !",
        f"On pensait être tranquilles... et voilà que @{member.display_name} arrive 😬",
    ]

    await welcome_channel.send(random.choice(messages))


@bot.event
async def on_voice_state_update(member, before, after):
    if (
        after.channel
        and after.channel.name == "➕・CRÉER UN SALON"
        and after.channel.category.name.startswith(("↽🎮・Gaming", "↽💬・Forum"))
    ):
        await create_channel(member)
        print(f"✅ Salon de {member.display_name} créé avec succès")
    if (
        before.channel
        and before.channel.name.endswith("'s Palace")
        and len(before.channel.members) == 0
    ):
        await before.channel.delete()
        print(f"🗑️ Salon de {member.display_name} à été supprimé pour cause d'inativité")


async def create_channel(member):
    guild = member.guild
    overwrites = {
        member: discord.PermissionOverwrite(
            # General Permissions
            view_channel=True,
            manage_channels=True,
            manage_permissions=True,
            manage_webhooks=True,
            # Members Permissions
            create_instant_invite=True,
            # Voice Channels Permissions
            connect=True,
            speak=True,
            stream=True,
            use_soundboard=True,
            use_external_sounds=True,
            use_voice_activation=True,
            priority_speaker=True,
            mute_members=True,
            deafen_members=True,
            move_members=True,
            # Chat Voice Channels Permissions
            send_messages=True,
            embed_links=True,
            attach_files=True,
            add_reactions=True,
            use_external_emojis=True,
            use_external_stickers=True,
            mention_everyone=True,
            manage_messages=True,
            read_message_history=True,
            send_tts_messages=True,
            send_voice_messages=True,
            create_polls=True,
            # Events Permissions
            create_events=True,
            manage_events=True,
            # Applications Permissions
            use_application_commands=True,
            use_embedded_activities=True,
            use_external_apps=True,
        )
    }

    category = member.voice.channel.category
    if category:
        new_channel = await guild.create_voice_channel(
            name=f"{member.display_name}'s Palace",
            category=category,
            overwrites=overwrites,
        )
        await member.move_to(new_channel)


def load_sent_games():
    if not os.path.exists(SENT_GAMES_FILE):
        save_sent_games()

    with open(SENT_GAMES_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            return []
        return json.loads(content)

    return []


def save_sent_games(sent_games):
    while len(sent_games) > MAX_GAMES_STORE:
        sent_games.pop(0)

    with open(SENT_GAMES_FILE, "w", encoding="utf-8") as file:
        json.dump(sent_games, file, indent=4, ensure_ascii=False)


@tasks.loop(hours=12)
async def check_free_games():
    # DEV : 1336403452988751902    PROD : 977236274974978109
    channel: discord.TextChannel = bot.get_channel(1336403452988751902)
    games = steam.get_free_games()
    games += gog.get_free_games()
    games += epic.get_free_games()

    sent_games = load_sent_games()
    new_games = [game for game in games if game["link"] not in sent_games]

    if not new_games:
        print("🛑 Aucun nouveau jeu à envoyer")
        return

    for game in new_games:
        message = []
        message.append(f"Nouveau jeu **gratuit** sur **{game['platform']}** ! 🤑")
        message.append(f"**{game['title']}**")
        if game["expired_date"] != None:
            try:
                dt = datetime.strptime(game["expired_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_date = dt.strftime("%d/%m/%Y %H:%M:%S")
                message.append(f"\n_Offre limitée jusqu'au **{formatted_date}** !_")
            except ValueError:
                message.append(
                    f"\n_Offre limitée jusqu'au **{game['expired_date']}** !_"
                )
        message.append(f"\n{game['link']}")

        message = "\n".join(message)
        await channel.send(message)

    sent_games.extend(game["link"] for game in new_games)
    save_sent_games(sent_games)

    print(f"📩 {len(new_games)} nouveaux jeux envoyé sur {channel.name}")


if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("❌ ERROR : Le token Discord est manquant !")
    exit(1)
