import discord
from discord.ext import commands
import asyncio

from decouple import config 

from help_cog import help_cog
from music_cog import music_cog

# configurar el bot usando bot y cogs
# Cogs -> https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html


intents = discord.Intents.all() # discord.Intents.default()  vs discord.Intents.all() : https://discordpy.readthedocs.io/en/stable/api.html#discord.Intents.all

bot = commands.Bot(command_prefix='$', intents=intents) # !play


bot.remove_command('help') # da error si no se remueve el comando por defecto

def test_search_yt():
    music_cog_obj = music_cog(bot)

    # Test case 1: Valid search query
    item = "song name"
    result = music_cog_obj.search_yt(item)
    assert result is not False, "Test case 1 failed"


    # Test case 3: Empty search query
    item = ""
    result = music_cog_obj.search_yt(item)
    assert result is False, "Test case 3 failed"

    # Test case 4: Numeric search query
    item = "12345"
    result = music_cog_obj.search_yt(item)
    assert result is not False, "Test case 4 failed"

    # Test case 5: Special characters in search query
    item = "!@#$%^&*()"
    result = music_cog_obj.search_yt(item)
    assert result is not False, "Test case 5 failed"

    print("All test cases passed")

test_search_yt()