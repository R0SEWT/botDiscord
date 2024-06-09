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


async def main():
    async with bot:
        await bot.add_cog(help_cog(bot))
        await bot.add_cog(music_cog(bot))
        await bot.start(config('BOT_TOKEN'))

asyncio.run(main()) # asyncio concurrente code con async/await