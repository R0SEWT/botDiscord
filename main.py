'''
1. Extraer la URL del audio de Spotify: Usa la API de Spotify para obtener la URL del archivo de audio. [ x ]
2. Descargar el archivo de audio: Usa una herramienta como youtube-dl o spotdl para descargar la canción.
3. Reproducir el audio en Discord: Usa una librería como discord.py para conectarte y transmitir audio a un servidor de Discord.
Paso 1: Obtener la URL del audio de Spotify
Primero, necesitas obtener las credenciales de la API de Spotify y configurar un proyecto en Spotify Developer Dashboard.

'''

from decouple import config 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os



############################################## EXTRAER URL ########################################################


# Configurar las credenciales de la API de Spotify

client_id = config('ID_SPOTIFY') 
client_secret = config('SECRET_SPOTIFY')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Buscar la canción en Spotify

song_name = "paseo-estopa"
results = sp.search(q=song_name, limit=1)
track = results['tracks']['items'][0] # con esto se puede simular el comportamiento del FlaviBot
track_id = track['id']

# Obtener URL 
cancion = sp.track(track_id)
track_url = 'https://open.spotify.com/intl-es/track/' + track_id  # cyberpunk nanana

print(track_url)



############################################## DESCARGAR AUDIO ########################################################


# Descargar el archivo de audio: spotdl
# !pip install spotdl

os.system('spotdl ' + track_url) # !spotdl https://open.spotify.com/intl-es/track/3Z0oQ8r78OUaHvGPiDBR3W



############################################## REPRODUCIR AUDIO ########################################################

# Reproducir el audio en Discord: discord.py
# !pip install discord.py

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

TOKEN = config
bot = commands.Bot(command_prefix='!')

@bot.command()
async def play(ctx):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(FFmpegPCMAudio('paseo-estopa.mp3'))
    
bot.run(TOKEN)

# !python main.py

# !pip install -U discord.py[voice]
# !pip install -U youtube-dl

# !pip install -U spotipy
# !pip install -U python-dotenv

# !pip install -U ffmpeg-python

# !pip install -U discord.py[voice]




