"""
Cog de Interacciones: /felicitar, /regalo, /confesar, /ruleta_rusa, /derrotado, /decodifica
Comandos divertidos de interacción entre usuarios
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
import random
import asyncio

class InteractionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.decodifica_active = {}  # Almacenar juegos activos
    
    # ============== FELICITAR ==============
    
    @app_commands.command(name="felicitar", description="Felicita a otro usuario de forma bonita")
    @app_commands.describe(usuario="El usuario a felicitar", razon="Razón de la felicitación")
    async def felicitar(self, interaction: discord.Interaction, usuario: discord.User, razon: str = "Por ser increíble"):
        """Enviar una felicitación bonita a otro usuario"""
        
        felicitaciones = [
            "¡Lo hiciste increíble!",
            "¡Eres una estrella!",
            "¡Simplemente espectacular!",
            "¡Qué talento tienes!",
            "¡Merecido reconocimiento!",
        ]
        
        embed = discord.Embed(
            title="🎉 ¡Felicitaciones!",
            description=f"{interaction.user.mention} te felicita:",
            color=COLORS['purple']
        )
        
        embed.add_field(
            name="Razón",
            value=razon,
            inline=False
        )
        
        embed.add_field(
            name="Mensaje",
            value=random.choice(felicitaciones),
            inline=False
        )
        
        embed.set_thumbnail(url=usuario.avatar.url if usuario.avatar else None)
        embed.set_footer(text=f"Para: {usuario}")
        
        await interaction.response.send_message(
            content=f"{usuario.mention}",
            embed=embed
        )
    
    # ============== REGALO ==============
    
    @app_commands.command(name="regalo", description="Regala algo a otro usuario")
    @app_commands.describe(usuario="El usuario que recibirá el regalo", mensaje="Mensaje adicional")
    async def regalo(self, interaction: discord.Interaction, usuario: discord.User, mensaje: str = "Un regalo especial"):
        """Regala algo a otro usuario con efecto visual"""
        
        regalos = [
            "🎁 Una caja de chocolates",
            "🌹 Un hermoso ramo de flores",
            "🎮 Un videojuego nuevo",
            "📚 Un libro interesante",
            "🎵 Un álbum de música",
            "☕ Una taza de café especial",
            "🍰 Un delicioso pastel",
            "💎 Una joya especial",
            "🎭 Entradas al cine",
            "🚀 Un viaje sorpresa",
        ]
        
        regalo_random = random.choice(regalos)
        
        embed = discord.Embed(
            title="🎀 ¡Regalo!",
            description=f"{interaction.user.mention} te envía un regalo:",
            color=COLORS['info']
        )
        
        embed.add_field(
            name="Regalo",
            value=regalo_random,
            inline=False
        )
        
        embed.add_field(
            name="Mensaje",
            value=mensaje,
            inline=False
        )
        
        embed.set_thumbnail(url=usuario.avatar.url if usuario.avatar else None)
        embed.set_footer(text=f"Para: {usuario}")
        
        await interaction.response.send_message(
            content=f"{usuario.mention} ✨",
            embed=embed
        )
    
    # ============== CONFESAR ==============
    
    @app_commands.command(name="confesar", description="Haz una confesión anónima")
    @app_commands.describe(confesion="Tu confesión secreta")
    async def confesar(self, interaction: discord.Interaction, confesion: str):
        """Enviar una confesión anónima al canal"""
        
        # Buscar canal de confesiones o usar el actual
        canal = interaction.channel
        
        embed = discord.Embed(
            title="💭 Confesión Anónima",
            description=confesion,
            color=COLORS['warning']
        )
        
        embed.set_footer(text="Esta confesión es completamente anónima")
        
        await interaction.response.send_message(
            "✅ Confesión enviada de forma anónima",
            ephemeral=True
        )
        
        # Enviar la confesión al canal actual (sin mostrar quién la escribió)
        await canal.send(embed=embed)
    
    # ============== RULETA RUSA ==============
    
    @app_commands.command(name="ruleta_rusa", description="Juega a la ruleta rusa (50% de ganar/perder)")
    async def ruleta_rusa(self, interaction: discord.Interaction):
        """Juega a la ruleta rusa: 50% de sobrevivir, 50% de perder"""
        
        await interaction.response.defer()
        
        # Esperar 2 segundos para dramatismo
        await asyncio.sleep(2)
        
        resultado = random.choice([True, False])
        
        if resultado:
            embed = discord.Embed(
                title="🔫 Ruleta Rusa",
                description=f"✅ {interaction.user.mention} ¡SOBREVIVIÓ!",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Resultado",
                value="¡Tuviste suerte! La pistola estaba vacía en esta cámara.",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="🔫 Ruleta Rusa",
                description=f"❌ {interaction.user.mention} ¡PERDIÓ!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Resultado",
                value="Desafortunadamente, esta fue la cámara cargada.",
                inline=False
            )
        
        await interaction.followup.send(embed=embed)
    
    # ============== DERROTADO ==============
    
    @app_commands.command(name="derrotado", description="Menciona a alguien diciendo que perdió")
    @app_commands.describe(usuario="El usuario 'derrotado'", razon="Razón de la derrota")
    async def derrotado(self, interaction: discord.Interaction, usuario: discord.User, razon: str = "No aguantó"):
        """Mencionar a alguien diciendo que perdió"""
        
        derrotas = [
            "quedó fuera de combate",
            "no pudo seguir",
            "se rindió",
            "no dio la talla",
            "cayó estrepitosamente",
            "fue eliminado",
            "no resistió",
            "falló miserablemente",
        ]
        
        derrota_random = random.choice(derrotas)
        
        embed = discord.Embed(
            title="💔 ¡DERROTADO!",
            description=f"{usuario.mention} ha sido derrotado",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="Razón",
            value=f"{derrota_random}: {razon}",
            inline=False
        )
        
        embed.add_field(
            name="Ganador",
            value=interaction.user.mention,
            inline=False
        )
        
        embed.set_thumbnail(url=usuario.avatar.url if usuario.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    # ============== DECODIFICA ==============
    
    @app_commands.command(name="decodifica", description="Juego: el bot desordena palabras y debes ordenarlas")
    async def decodifica(self, interaction: discord.Interaction):
        """Mini-juego: Palabras desordenadas que deben ser ordenadas"""
        
        palabras = [
            ("PYTHON", "NOHTYP"),
            ("DISCORD", "DCORSDI"),
            ("SERVIDOR", "RODIVRES"),
            ("ADMINISTRADOR", "RODATSINIMDEA"),
            ("PROGRAMADOR", "RODARGORP"),
            ("VIDEOJUEGO", "OGEUJOEDIV"),
            ("DESARROLLO", "OLLORRASED"),
            ("PROGRAMACIÓN", "NÓICAMARGORP"),
            ("ALGORITMO", "OMTIROGLА"),
            ("FUNCIÓN", "NÓICNUF"),
        ]
        
        palabra_correcta, palabra_desordenada = random.choice(palabras)
        
        # Guardar el juego activo
        game_id = f"{interaction.user.id}_{interaction.channel.id}"
        self.decodifica_active[game_id] = {
            "palabra": palabra_correcta,
            "usuario": interaction.user.id,
            "timeout": False
        }
        
        embed = discord.Embed(
            title="🔤 Decodifica",
            description="Ordena las letras para formar la palabra correcta",
            color=COLORS['info']
        )
        
        embed.add_field(
            name="Palabra Desordenada",
            value=f"`{palabra_desordenada}`",
            inline=False
        )
        
        embed.add_field(
            name="Instrucciones",
            value="Tienes **30 segundos** para escribir la palabra correctamente",
            inline=False
        )
        
        embed.set_footer(text=f"Juego iniciado por {interaction.user}")
        
        await interaction.response.send_message(embed=embed)
        
        # Esperar 30 segundos
        try:
            # Esperar por un mensaje del usuario
            def check(message):
                return (
                    message.author == interaction.user and 
                    message.channel == interaction.channel
                )
            
            message = await self.bot.wait_for("message", check=check, timeout=30)
            
            if message.content.upper() == palabra_correcta:
                embed_win = discord.Embed(
                    title="✅ ¡Correcto!",
                    description=f"{interaction.user.mention} acertó la palabra",
                    color=discord.Color.green()
                )
                embed_win.add_field(
                    name="Palabra",
                    value=f"`{palabra_correcta}`",
                    inline=False
                )
                embed_win.add_field(
                    name="Tiempo",
                    value=f"Respondiste en {30 - int(message.created_at.timestamp() - interaction.created_at.timestamp())} segundos",
                    inline=False
                )
                
                await message.reply(embed=embed_win)
            else:
                embed_lose = discord.Embed(
                    title="❌ Incorrecto",
                    description=f"La respuesta era: `{palabra_correcta}`",
                    color=discord.Color.red()
                )
                
                await message.reply(embed=embed_lose)
        
        except asyncio.TimeoutError:
            embed_timeout = discord.Embed(
                title="⏰ ¡Tiempo Agotado!",
                description=f"La palabra era: `{palabra_correcta}`",
                color=COLORS['warning']
            )
            
            await interaction.channel.send(embed=embed_timeout)
        
        finally:
            # Limpiar el juego activo
            if game_id in self.decodifica_active:
                del self.decodifica_active[game_id]


async def setup(bot):
    await bot.add_cog(InteractionsCog(bot))
