import discord # basicly boty
import asyncio
import random
from discord.ext import commands
from mutagen.mp3 import MP3 # meta dane plików mp3

# Disclamer:
# Pisane szybko i nie uważnie, coś może nie działać. Jeżeli czytasz moje komentarze to spodziewaj się błędów językowych XDDD


# Podstawowe info
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
TOKEN = ''  # token z dev portalu discorda
POCZEKALNIA_ID =   # ID kanału "Poczekalnia" lub inaczej go tam sobie nazwij
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# uprawnienia bota!-
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
# dodane emotikony dla czytelności / podstawowy handling
async def on_ready():
    print(f'✅ Zalogowano jako {bot.user.name}')
    channel = bot.get_channel(POCZEKALNIA_ID)
    if channel:
        try:
            await channel.connect()
            print(f'🎧 Dołączono do kanału: {channel.name}')
        except discord.ClientException:
            print(f'⚠️ Bot już połączony z kanałem głosowym.')
    else:
        print("❌ Nie znaleziono kanału 'Poczekalnia'.")

# funkcja która sprawdza długość pliku mp3
def get_mp3_duration(file):
    audio = MP3(file)
    mp3time = int(audio.info.length)
    return mp3time

#
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if after.channel and after.channel.id == POCZEKALNIA_ID:
        print(f' {member.name} dołączył do Poczekalni')

        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if not voice_client or not voice_client.is_connected():
            channel = bot.get_channel(POCZEKALNIA_ID)
            voice_client = await channel.connect()

        if not voice_client.is_playing():
            # Losowanie pliku audio
            audio_files = ["infolinia.mp3", "infolinia_drop1.mp3"] # 2 pliki audio jeden to easter egg
            weights = [80, 20]  # wagi do losowania
            selected_file = random.choices(audio_files, weights=weights, k=1)[0]

            mp3time = get_mp3_duration(selected_file)
            source = discord.FFmpegPCMAudio(selected_file)
            voice_client.play(source)
            print(f"🔊 Odtwarzanie pliku: {selected_file}")

        await asyncio.sleep(mp3time) #Odczekuje czas do zakończenia (tak okropna metoda można by było zakończyć po zgłoszeniu przez ffmpeg process 0 ale mi się nie chcę co mi zrobisz huh?)

        other_channels = [
            ch for ch in member.guild.voice_channels if ch.id != POCZEKALNIA_ID
        ]

        if not other_channels:
            print("⚠️ Brak innych kanałów do przeniesienia.")
            return

        max_users = max(len(ch.members) for ch in other_channels)
        candidates = [ch for ch in other_channels if len(ch.members) == max_users]
        target_channel = random.choice(candidates)

        await member.move_to(target_channel)
        print(f'➡️ Przeniesiono {member.name} na kanał {target_channel.name}')

#Start
bot.run(TOKEN)
