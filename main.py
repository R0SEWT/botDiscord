'''
1. Extraer la URL del audio de Spotify: Usa la API de Spotify para obtener la URL del archivo de audio.
2. Descargar el archivo de audio: Usa una herramienta como youtube-dl o spotdl para descargar la canción.
3. Reproducir el audio en Discord: Usa una librería como discord.py para conectarte y transmitir audio a un servidor de Discord.
Paso 1: Obtener la URL del audio de Spotify
Primero, necesitas obtener las credenciales de la API de Spotify y configurar un proyecto en Spotify Developer Dashboard.

'''

from decouple import config 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Configurar las credenciales de la API de Spotify

client_id = config('ID_SPOTIFY') 
client_secret = config('SECRET_SPOTIFY')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Buscar la canción en Spotify

song_name = "malamante"
results = sp.search(q=song_name, limit=1)
track = results['tracks']['items'][0]
track_id = track['id']

# Obtener URL 

track_url = sp.track(track_id)

print(track_url['uri'])
print('https://open.spotify.com/intl-es/track/' + track_id) # cyberpunk nanana








