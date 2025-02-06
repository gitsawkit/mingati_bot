import discord, os, random
from discord.ext import commands


DISCORD_TOKEN = os.getenv("DISCORD_SECRET_CLIENT")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    print(f"💬 Message de {message.author}: {message.content}")

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
    welcome_channel: discord.TextChannel = bot.get_channel(933379075995758603)

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

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.name == "➕・CRÉER UN SALON" and after.channel.category.name.startswith(("↽🎮・Gaming", "↽💬・Forum")):
        await create_channel(member)
        print(f"👌 Salon de {member.display_name} créé avec succès")
    if before.channel and before.channel.name.startswith(f"{member.display_name}'s Palace") and len(before.channel.members) == 0:
            await before.channel.delete()
            print(f"🗑️ Salon de {member.display_name} à été supprimé pour cause d'inativité")

async def create_channel(member):
    guild = member.guild
    overwrites = {
        member: discord.PermissionOverwrite(
            # General Permissions
            view_channel = True,
            manage_channels = True,
            manage_permissions = True,
            manage_webhooks = True,
            # Members Permissions
            create_instant_invite = True,
            # Voice Channels Permissions
            connect = True,
            speak = True,
            stream = True,
            use_soundboard = True,
            use_external_sounds = True,
            use_voice_activation = True,
            priority_speaker = True,
            mute_members = True,
            deafen_members = True,
            move_members = True,
            # Chat Voice Channels Permissions
            send_messages = True,
            embed_links = True,
            attach_files = True,
            add_reactions = True,
            use_external_emojis = True,
            use_external_stickers = True,
            ## USE SON EXTERNE
            mention_everyone = True,
            manage_messages = True,
            read_message_history = True,
            send_tts_messages = True,
            send_voice_messages = True,
            create_polls = True,
            # Events Permissions
            create_events = True,
            manage_events = True,
            # Applications Permissions
            use_application_commands = True,
            use_embedded_activities = True,
            use_external_apps = True,
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


if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("❌ ERROR : Le token Discord est manquant !")
    exit(1)