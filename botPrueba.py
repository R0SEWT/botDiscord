# This example requires the 'message_content' intent.

import discord
from decouple import config

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready(): #  Dado que esta biblioteca es asincrónica, hacemos las cosas al estilo de una "devolución de llamada" (callback)
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'): # !play
        await message.channel.send('hail Hitler!')

client.run(config('BOT_TOKEN'))
