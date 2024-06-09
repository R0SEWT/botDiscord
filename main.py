'''
1. Extraer la URL del audio de Spotify: Usa la API de Spotify para obtener la URL del archivo de audio.
2. Descargar el archivo de audio: Usa una herramienta como youtube-dl o spotdl para descargar la canción.
3. Reproducir el audio en Discord: Usa una librería como discord.py para conectarte y transmitir audio a un servidor de Discord.
Paso 1: Obtener la URL del audio de Spotify
Primero, necesitas obtener las credenciales de la API de Spotify y configurar un proyecto en Spotify Developer Dashboard.

'''

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configurar las credenciales de la API de Spotify


