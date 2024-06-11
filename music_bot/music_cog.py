import discord
from discord.ext import commands

from youtube_dl import YoutubeDL # eliminar una linea en el paquete yt_dlp tras instalar


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False 
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}  # opciones para youtube-dl (no reproducir listas de reproducción)
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} 

        self.vc = None # cliente de voz


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl: #  with -> cierra el recurso automaticamente
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
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) # reproducir el audio
        else:
            self.is_playing = False

    async def play_music(self, ctx): 
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source'] # url 
            if self.vc == None or not self.vc.is_connected(): # no entiendo como el bot no estaria conectado, pero bueno
                try:
                    self.vc = await self.music_queue[0][1].connect() # (espera que se conecte al vc) (m_q[0][1] -> vc del primer elemento de la cola
                except Exception as e:
                    await  ctx.send("voice channel inconectable, meper?") # aqui usamos el canal de voz del 
                    print(e)
                    return
                await ctx.send(f"Reproduciendo: {self.music_queue[0][0]['title']}")
            else:
                if self.vc.is_playing():
                    self.vc.stop()
                self.vc = await self.vc.move_to(self.music_queue[0][1]) # que se mueva al canal de voz de la cola
                await ctx.send(f"Reproduciendo: {self.music_queue[0][0]['title']}")
           
            self.music_queue.pop(0) 
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) 

        else:
            self.is_playing = False
    
    @commands.command(name="play", aliases=["p"], help="Reproduce terrible cancion desde YT")
    async def play(self, ctx, *args): # *args -> argumentos variables, ctx -> contexto del comando
        #await ctx.send("Buscando la cancion, un momento por favor")
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel # vc del comandante
        print(voice_channel)

        if voice_channel is None:
            await ctx.send("Mira mijo no puedo reproducirme en el eter, conectate a un canal")
        else:
            song = self.search_yt(query) # buscar la canción en YT
            if type(song) == type(True): # si la busqueda falla (no se encuentra la cancion) 
                await ctx.send("O YT no tiene la cancion o no tengo internet, no se cual de las dos es peor")
                await ctx.send("Si quieres que te diga la verdad, no tengo internet")
                print("No se encontro la cancion")
            else:
                await ctx.send(f"Encolando: {song['title']}")
                self.music_queue.append([song, voice_channel])
                print("Encolado")
                if self.is_playing == False:
                    await self.play_music(ctx)
                    print("Reproduciendo")

    @commands.command(name="pause", aliases=["s"], help="Pausa la musica")
    async def pause(self, ctx, *args):
        if self.vc.is_playing():
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send("Basta")

        elif self.is_paused:
            self.vc.resume()
            self.is_paused = False
            await ctx.send("Reanudando")
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
            await self.self.play_music(ctx)
            await ctx.send("Pasando la cancion")

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