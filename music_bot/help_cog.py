import discord
from discord.ext import commands

# Te tira tu help maldito
class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"], help="Te tira un help maldito")
    async def help(self, ctx):
        help_embed = discord.Embed(
            title="Ayuda",
            description="Estos son los comandos que puedes usar",
            color=discord.Color.green()
        )

        help_embed.add_field(name="help", value="Cosorro recursividad")
        help_embed.add_field(name="play", value="Reproduce una canción de YouTube")
        help_embed.add_field(name="pause", value="Pausa la música")
        help_embed.add_field(name="resume", value="Reanuda la música")
        help_embed.add_field(name="skip", value="Salta a la siguiente canción")
        help_embed.add_field(name="queue", value="Te muestra la cola")
        help_embed.add_field(name="clear", value="Borra la cola ")
        help_embed.add_field(name="leave", value="Patea al bot del canal de voz")

        await ctx.send(embed=help_embed)