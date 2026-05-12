"""
Cog de Integraciones: /stats (Minecraft), /tiktok, /youtube, /tiktok-agregar, /youtube-agregar
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
from database import add_social_link, get_social_link
import aiohttp
import json

class IntegrationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ============== MINECRAFT STATS ==============
    
    @app_commands.command(name="stats", description="Ver stats de Minecraft (NameMC)")
    @app_commands.describe(usuario="Username de Minecraft")
    async def stats(self, interaction: discord.Interaction, usuario: str):
        """Obtener stats de NameMC"""
        await interaction.response.defer()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.namemc.com/profile/{usuario}") as resp:
                    if resp.status != 200:
                        await interaction.followup.send(
                            f"Usuario '{usuario}' no encontrado",
                            ephemeral=True
                        )
                        return
                    
                    data = await resp.json()
            
            embed = discord.Embed(
                title=f"Stats de {data.get('name', usuario)}",
                color=COLORS['info']
            )
            
            # Skin del jugador
            skin_url = f"https://crafatar.com/avatars/{data.get('id', '')}?size=64"
            embed.set_thumbnail(url=skin_url)
            
            embed.add_field(name="UUID", value=data.get('id', 'N/A'), inline=False)
            embed.add_field(name="Username", value=data.get('name', 'N/A'), inline=True)
            
            # Historial de nombres (últimos 3)
            if 'nameHistory' in data and data['nameHistory']:
                names = [item.get('name', '') for item in data['nameHistory'][-3:]]
                embed.add_field(name="Nombres Anteriores", value=", ".join(names) or "Ninguno", inline=False)
            
            embed.set_image(url=f"https://crafatar.com/renders/body/{data.get('id', '')}")
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            await interaction.followup.send(
                f"Error obteniendo stats: {str(e)}",
                ephemeral=True
            )
    
    # ============== TIKTOK AGREGAR ==============
    
    @app_commands.command(name="tiktok_agregar", description="Agregar TikTok al servidor (solo owner)")
    @app_commands.describe(usuario="Username de TikTok", url="URL del perfil TikTok")
    async def tiktok_agregar(self, interaction: discord.Interaction, usuario: str, url: str):
        """Agregar enlace de TikTok (solo owner)"""
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(
                "Solo el dueño del servidor puede usar este comando",
                ephemeral=True
            )
            return
        
        success = add_social_link(
            interaction.guild.id,
            "tiktok",
            usuario,
            url,
            interaction.user.id
        )
        
        if success:
            await interaction.response.send_message(
                f"TikTok agregado: {usuario}",
                ephemeral=False
            )
        else:
            await interaction.response.send_message(
                "Ya existe un TikTok configurado en este servidor",
                ephemeral=True
            )
    
    # ============== TIKTOK VER ==============
    
    @app_commands.command(name="tiktok", description="Ver perfil de TikTok del servidor")
    async def tiktok(self, interaction: discord.Interaction):
        """Mostrar perfil de TikTok configurado"""
        result = get_social_link(interaction.guild.id, "tiktok")
        
        if not result:
            await interaction.response.send_message(
                "No hay TikTok configurado en este servidor",
                ephemeral=True
            )
            return
        
        _, _, usuario, url, _, _ = result
        
        embed = discord.Embed(
            title="TikTok del Servidor",
            description=f"Síguenos en TikTok: [@{usuario}]({url})",
            color=0x000000
        )
        
        embed.add_field(name="Usuario", value=f"@{usuario}", inline=True)
        embed.add_field(name="Link", value=f"[Ir al perfil]({url})", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    # ============== YOUTUBE AGREGAR ==============
    
    @app_commands.command(name="youtube_agregar", description="Agregar YouTube al servidor (solo owner)")
    @app_commands.describe(canal="Nombre del canal", url="URL del canal YouTube")
    async def youtube_agregar(self, interaction: discord.Interaction, canal: str, url: str):
        """Agregar enlace de YouTube (solo owner)"""
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(
                "Solo el dueño del servidor puede usar este comando",
                ephemeral=True
            )
            return
        
        success = add_social_link(
            interaction.guild.id,
            "youtube",
            canal,
            url,
            interaction.user.id
        )
        
        if success:
            await interaction.response.send_message(
                f"YouTube agregado: {canal}",
                ephemeral=False
            )
        else:
            await interaction.response.send_message(
                "Ya existe un YouTube configurado en este servidor",
                ephemeral=True
            )
    
    # ============== YOUTUBE VER ==============
    
    @app_commands.command(name="youtube", description="Ver canal de YouTube del servidor")
    async def youtube(self, interaction: discord.Interaction):
        """Mostrar canal de YouTube configurado"""
        result = get_social_link(interaction.guild.id, "youtube")
        
        if not result:
            await interaction.response.send_message(
                "No hay YouTube configurado en este servidor",
                ephemeral=True
            )
            return
        
        _, _, canal, url, _, _ = result
        
        embed = discord.Embed(
            title="YouTube del Servidor",
            description=f"Suscríbete a nuestro canal: [{canal}]({url})",
            color=0xFF0000
        )
        
        embed.add_field(name="Canal", value=canal, inline=True)
        embed.add_field(name="Link", value=f"[Ir al canal]({url})", inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(IntegrationsCog(bot))
