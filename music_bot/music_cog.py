import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False 
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}  # Investigar
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} 

        self.vc = None # cliente de voz


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl: # withc -> ciere automatico
            try: 
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0] # solo extrae, no descargar
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source'] 
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx): 
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source'] # url 
            if self.vc == None or not self.vc.is_connected(): # no entiendo como el bot no estaria conectado, pero bueno
                self.vc = await self.music_queue[0][1].connect() # (espera que se conecte al vc) (m_q[0][1] -> vc del primer elemento de la cola
                if self.vc == None:
                    await  ctx.send("voice channel inconectable, meper?") # aqui usamos el canal de voz del 
                    return
            else:
                self.vc = await self.vc.move_to(self.music_queue[0][1]) # si ya está conectado, movemos al bot al canal de voz del primer elemento de la cola

            print(self.music_queue)
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) # reproducir el audio

        else:
            self.is_playing = False
    
    @commands.command(name="play", aliases=["p"], help="Reproduce terrible cancion desde YT")
    async def play(self, ctx, *args): # *args -> argumentos variables, ctx -> contexto del comando
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel # vc del comandante

        if voice_channel is None:
            await ctx.send("Mira mijo no puedo reproducirme en el eter, conectate a un canal")
        else:
            song = self.search_yt(query) # buscar la canción en YT
            if type(song) == type(True):
                await ctx.send("O YT no tiene la cancion o no tengo internet, no se cual de las dos es peor")
                await ctx.send("Si quieres que te diga la verdad, no tengo internet")
            else:
                await ctx.send(f"Encolando: {song['title']}")
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", aliases=["s"], help="Pausa la musica")
    async def pause(self, ctx, *args):
        if self.vc.is_playing():
            self.is_playing = False
            self.is_paused = True
            self.vc.pause() 
            await ctx.send("Basta")

        elif self.is_paused:
            self.vc.resume()
        else:
            await ctx.send("Que musica?")

    @commands.command(name="resume", aliases=["r"], help="Reanuda la musica")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()
            self.is_paused = False
            await ctx.send("Reanudando")
        else:
            await ctx.send("No hay nada que reanudar")


    @commands.command(name="skip", aliases=['ag'], help='Reproduce la siguiente cancion de la cola')
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name='cola', aliases = ['q'], help = 'Te muestra la cola ;)')
    async def queue(self, ctx):
        sq = ''
        sample = 4

        for i in range(0, len(self.music_queue)):
            if i > sample: break
            sq += self.music_queue[i][0]['title'] + '\n'
        
        if sq != '':
            await ctx.send(sq)
        else:
            await ctx.send('No tengo cola :c')


    @commands.command(name='clear', aliases=['c', 'barre'], help='Detiene la cancion y limpia la cola')
    async def clear (self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send('El chiste es muy facil')

    @commands.command(name='leave', aliases=['l'], help='Patea al bot del canal de voz')
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await ctx.send()
        await self.vc.disconnect()